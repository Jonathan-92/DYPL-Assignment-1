# -*- coding: cp1252 -*-
import JythonTranslater
import re
import math

class program(JythonTranslater.Jtrans):
	
	REGEX_PEN_DOWN 		= "\s*pen down\s*\n"
	REGEX_PEN_UP		= "\s*pen up\n"
	REGEX_MOVE_FORWARD	= "\s*move forward\n"
	REGEX_MOVE_BACKWARD	= "\s*move backward\n"
	REGEX_MOVE			= "\s*move\(\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*,\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*\)"
	REGEX_TURN_CW		= "\s*turn cw\(\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*\)"
	REGEX_TURN_CCW		= "\s*turn ccw\(\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*\)"
	REGEX_PUT			= "\s*put\(\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*,\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*,\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*\)"
	REGEX_FOR = "\s*for\s\w*\s*=\s*\d*\s*to\s*\d*\s*do"
	
	pen_down = False
	
	pen_pos_x = 0
	pen_pos_y = 0
	pen_angle = 0
		
	def actionPerformed(self, event):
		str = self.dypl.getCode()
		stmts = str.split("\n") 
		self.doStatements(stmts)
	
	def doStatements(self, stmts):
	
		index = 0
		while index < len(stmts):
			stmt = stmts[index]
			
			if self.regex(stmt, self.REGEX_PEN_DOWN): # regex är en metod som kollar om item matchar regexet för penDown etc.
				self.penDown()
				
			elif self.regex(stmt, self.REGEX_PEN_UP):
				self.penUp()
			
			elif self.regex(stmt, self.REGEX_MOVE_FORWARD):
				self.moveForward()
				
			elif self.regex(stmt, self.REGEX_MOVE_BACKWARD):
				self.moveBackward()

			elif self.regex(stmt, self.REGEX_MOVE):
				param = self.getParamsAsString(stmt)	
				eval("self.move("+param+")")
			
			elif self.regex(stmt, self.REGEX_TURN_CW):
				param = self.getParamsAsString(stmt)
				eval("self.turnCW("+param+")")

			elif self.regex(stmt, self.REGEX_TURN_CCW):
				param = self.getParamsAsString(stmt)
				eval("self.turnCCW("+param+")")

			elif self.regex(stmt, self.REGEX_PUT):
				param = self.getParamsAsString(stmt)
				eval("self.put("+param+")")

			elif self.regex(stmt, self.REGEX_FOR):
				params = stmt.split("\s*")		#splits the header of the for-loop
				var_name = params[1]			#gets the variable name 
				var = int(params[3])			#gets the variable value				
				target = int(params[6])			#gets target value
				
				endOfLoop = stmts.find("end",index) #gets line number where loop finishes

				if endOfLoop < 0:
					print "for-loop without 'end'"		#if there is'nt an "end" an error message appears and the method stops
					break
				
				self.forLoop(var_name, var, target, stmts[index:endOfLoop]) #all rows between where we are and "end" is sent
				index = endOfLoop 	#we move to the "end" statement
				
			else:
				print self.unknownCommand(stmt)
			
			index = index + 1
	
	def forLoop(self, var_name, value, to, *stmts):
		new_statements = []							#to be sent to doStatements
		for index in xrange(value, to):				#executes all statements the requested # of times			
			for index2 in xrange(len(stmts)):			#replaces variables with a value
				new_statements[index2] = stmts[index2].replace(var_name, index)
			
			self.doStatements(new_statements)
	
	def getParamsAsString(self, stmt):
		return stmt[stmt.find("(")+1 : stmt.rfind(")")]		#returns the substring between the parantesis'
	
	def move(self, steps, angle):
		print "move begin"
		new_dir = self.pen_angle + angle
		new_x = self.pen_pos_x + steps * math.sin(new_dir)
		new_y = self.pen_pos_y + steps * math.cos(new_dir)
		
		if self.pen_down:
			plotLine(self.pen_pos_x, self.pen_pos_y, new_x, new_y)
			
		self.pen_pos_x = new_x
		self.pen_pos_y = new_y
		self.pen_angle = new_dir
		print "move end"
		
	def moveBackward(self):
		pass
		
	def moveForward(self):
		pass
	
	def penDown(self):
		pen_down = True
	
	def penUp(self):
		pen_down = False

	def plotLine(x0,y0, x1,y1):
		dx=x1-x0
		dy=y1-y0

		D = 2*dy - dx
		DYPL.setPixel(x0,y0)
		y=y0

		for x in xrange(x0+1, x1):
			if D > 0:
				y = y+1
				DYPL.setPixel(x,y)
				D = D + (2*dy-2*dx)
			else:
				DYPL.setPixel(x,y)
				D = D + (2*dy)
				
	def put(self, xpos, ypos, angle):
		pass
	
	def regex(self, stmt, method):
		return re.match(method, stmt)
	
	def setDYPL( self, obj ):
		self.dypl = obj
	
	def turnCW(self, angle):
		pass
		
	def turnCCW(self, angle):
		pass
		
	def unknownCommand(self, str):
		return str, " is an unknown command"
		
if __name__ == '__main__':
    import DYPL
    DYPL(program())
