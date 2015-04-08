# -*- coding: cp1252 -*-
import JythonTranslater
import re
import math

class program(JythonTranslater.Jtrans):
	
	REGEX_PEN_DOWN 		= "\s*pen down\s*"

	REGEX_PEN_UP		= "\s*pen up\s*"
	REGEX_MOVE_FORWARD	= "\s*move forward\s*"
	REGEX_MOVE_BACKWARD	= "\s*move backward\s*"
	REGEX_MOVE			= "\s*move\(\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*,\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*\)"
	REGEX_TURN_CW		= "\s*turn cw\(\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*\)"
	REGEX_TURN_CCW		= "\s*turn ccw\(\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*\)"
	REGEX_PUT			= "\s*put\(\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*,\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*,\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*\)\s*"
	REGEX_FOR = "\s*for\s[a-zA-Z]+\s=\s(0|([1-9]\d*))\sto\s(0|([1-9]\d*))\sdo\s*"
	
	pen_down = False
	
	pen_pos_x = 0
	pen_pos_y = 0
	pen_angle = 0
		
	def actionPerformed(self, event):
                for i in range(0, 301):
                        for j in range(0, 301):
                                self.dypl.unsetPixel(i, j)
		str = self.dypl.getCode()
		stmts = str.split("\n") 
		self.doStatements(stmts)
	
	def doStatements(self, stmts):
	
		index = 0
		while index < len(stmts):
			stmt = stmts[index].strip()
			
			if re.match(self.REGEX_PEN_DOWN, stmt):
				self.penDown()
				
			elif re.match(self.REGEX_PEN_UP, stmt):
				self.penUp()
			
			elif re.match(self.REGEX_MOVE_FORWARD, stmt):
				self.moveForward()
				
			elif re.match(self.REGEX_MOVE_BACKWARD, stmt):
				self.moveBackward()

			elif re.match(self.REGEX_MOVE, stmt):
				eval("self."+stmt)
			
			elif re.match(self.REGEX_TURN_CW, stmt):
				s = re.split("turn cw",stmt)
				eval("self.turnCW("+s[1]+")")

			elif re.match(self.REGEX_TURN_CCW, stmt):
				s = re.split("turn ccw",stmt)
				eval("self.turnCW("+s[1]+")")

			elif re.match(self.REGEX_PUT, stmt):
				eval("self."+stmt)

			elif re.match(self.REGEX_FOR, stmt):
				params = re.split("\s*", stmt)		#splits the header of the for-loop
				var_name = params[1]			#gets the variable name 
				var = int(params[3])			#gets the variable value
				target = int(params[5])			#gets target value

				#all rows between where we are and "end" is sent
				stmtCount = self.forLoop(var_name, var, target, stmts[index + 1:]) 
				index += stmtCount 	#we move to the "end" statement
			
			elif stmt == "":
				pass
			else:
				self.unknownCommand(stmt)
			
			index = index + 1
	
	def forLoop(self, var_name, value, to, stmts):
		stmtCount = 0
		for index in xrange(value, to):		#executes all statements the requested # of times			
                        new_statements = []			#to be sent to doStatements
                        stmtCount = 0
			for stmt in stmts:			
                                stmtCount += 1
                                if stmt == "end":
                                        break
                                #replaces variables with a value
				new_statements.append(stmt.replace(var_name, str(index)))
			self.doStatements(new_statements)
		return stmtCount
	
	def move2(self, steps, angle):
		print "move begin"
		new_dir = self.pen_angle + angle
		new_x = self.pen_pos_x + (steps * math.cos(math.radians(new_dir+90) ) )
		new_y = self.pen_pos_y + (steps * math.sin(math.radians(new_dir+90) ) )
		
		print str(new_x) + " " + str(new_y)
		
		if self.pen_down:
			self.plotLine(self.pen_pos_x, self.pen_pos_y, new_x, new_y)
			
		self.pen_pos_x = new_x
		self.pen_pos_y = new_y
		self.pen_angle = new_dir
		print "move end"
		
	def move(self, steps, angle):
		self.pen_angle += angle
		if steps < 1: return
		
		delta_x = math.cos(math.radians(self.pen_angle-90))
		delta_y = math.sin(math.radians(self.pen_angle-90))
		
		if self.penDown:
			positions_x = map(lambda x: self.pen_pos_x + x * delta_x, range( 1, steps + 1))
			positions_y = map(lambda y: self.pen_pos_y + y * delta_y, range( 1, steps + 1))
			
			for i in xrange(steps):
				self.dypl.setPixel( int(positions_x[i]), int(positions_y[i]) )
			
		self.pen_pos_x += steps * delta_x
		self.pen_pos_y += steps * delta_y
		
	def moveBackward(self):
		self.move(1, 180)
		self.turnCW(180)
		
	def moveForward(self):
		self.move(1, 0)
	
	def penDown(self):
		self.pen_down = True
		
	def penUp(self):
		self.pen_down = False

	def plotLine(self, x0,y0, x1,y1):
		print "plotLine ftw"
		dx=x1-x0
		dy=y1-y0

		D = 2*dy - dx
		self.dypl.setPixel(x0,y0)
		y=y0

		for x in range(x0, x1):
			if D > 0:
				y = y+1
				self.dypl.setPixel(x,y)
				D = D + (2*dy-2*dx)
			else:
				self.dypl.setPixel(x,y)
				D = D + (2*dy)
				
	def put(self, xpos, ypos, angle):
		self.pen_pos_x = xpos
		self.pen_pos_y = ypos
		self.pen_angle = angle		
	
	def setDYPL( self, obj ):
		self.dypl = obj
	
	def turnCW(self, angle):
		self.pen_angle += angle
		
	def turnCCW(self, angle):
		self.pen_angle -= angle
		
	def unknownCommand(self, str):
		print str, " is an unknown command"
		
if __name__ == '__main__':
    import DYPL
    DYPL(program())
