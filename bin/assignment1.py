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
	REGEX_PUT			= "\s*put\(\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*,\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*,\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*\)"
	REGEX_FOR = "\s*for\s\w*\s*=\s*\d*\s*to\s*\d*\s*do"
	
	pen_down = False
	
	pen_pos_x = 150
	pen_pos_y = 150
	pen_angle = 0
		
	def actionPerformed(self, event):
		str = self.dypl.getCode()
		stmts = str.split("\n") 
		self.doStatements(stmts)
	
	def doStatements(self, stmts):
	
		index = 0
		while index < len(stmts):
			stmt = stmts[index].strip()
			
			if re.match(stmt, self.REGEX_PEN_DOWN):
				self.penDown()
				
			elif re.match(stmt, self.REGEX_PEN_UP):
				self.penUp()
			
			elif re.match(stmt, self.REGEX_MOVE_FORWARD):
				self.moveForward()
				
			elif re.match(stmt, self.REGEX_MOVE_BACKWARD):
				self.moveBackward()

			elif re.match(stmt, self.REGEX_MOVE):
				eval("self."+stmt)
			
			elif re.match(stmt, self.REGEX_TURN_CW):
				s = re.split("turn cw",stmt)
				eval("self.turnCW("+s[1]+")")

			elif re.match(stmt, self.REGEX_TURN_CCW):
				s = re.split("turn ccw",stmt)
				eval("self.turnCW("+s[1]+")")

			elif re.match(stmt, self.REGEX_PUT):
				eval("self."+stmt)

			elif re.match(stmt, self.REGEX_FOR):
				params = stmt.split(" ")		#splits the header of the for-loop
				var_name = params[1]			#gets the variable name 
				var = int(params[3])			#gets the variable value				
				target = int(params[6])			#gets target value
				
				endOfLoop = stmts.find("end",index) #gets line number where loop finishes

				if endOfLoop < 0:
					print "for-loop without 'end'"		#if there is'nt an "end" an error message appears and the method stops
					break
				
				self.forLoop(var_name, var, target, stmts[index:endOfLoop]) #all rows between where we are and "end" is sent
				index = endOfLoop 	#we move to the "end" statement
			
			elif stmt == "":
				pass
			else:
				self.unknownCommand(stmt)
			
			index = index + 1
	
	def forLoop(self, var_name, value, to, *stmts):
		new_statements = []							#to be sent to doStatements
		for index in xrange(value, to):				#executes all statements the requested # of times			
			for index2 in xrange(len(stmts)):			#replaces variables with a value
				new_statements[index2] = stmts[index2].replace(var_name, index)
			
			self.doStatements(new_statements)
	
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
		delta_x = math.cos(math.radians(self.pen_angle + angle))
		delta_y = math.sin(math.radians(self.pen_angle + angle))
		
		if self.penDown:
			positions_x = map(lambda x: self.pen_pos_x + x*delta_x, range(steps))
			positions_y = map(lambda y: self.pen_pos_y + y*delta_y, range(steps))
			
			for i in xrange(steps):
				self.dypl.setPixel(int(positions_x[i]), int(positions_y[i]))
			
		self.pen_pos_x += steps * delta_x
		self.pen_pos_y += steps * delta_y
		self.pen_angle += angle
	def moveBackward(self):
		pass
		
	def moveForward(self):
		pass
	
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
		pass
	
	def setDYPL( self, obj ):
		self.dypl = obj
	
	def turnCW(self, angle):
		pass
		
	def turnCCW(self, angle):
		pass
		
	def unknownCommand(self, str):
		print str, " is an unknown command"
		
if __name__ == '__main__':
    import DYPL
    DYPL(program())
