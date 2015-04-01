# -*- coding: cp1252 -*-
import JythonTranslater

class program(JythonTranslater.Jtrans):
	
	pen_down = False
	
	pen_pos_x = 0.0
	pen_pos_y = 0.0
	pen_angle = 0
	
	def actionPerformed(self, event):
		str = self.dypl.getCode()
		stmts = str.split("\n")
		for stmt in stmts:
		
			if self.regex(stmt, self.penDown): # regex är en metod som kollar om item matchar regexet för penDown etc.
				self.penDown()
				
			elif self.regex(stmt, self.penUp):
				self.penUp()
			
			elif self.regex(stmt, self.moveForward):
				self.moveForward()
			elif self.regex(stmt, self.moveBackward):
				self.moveBackward()

			elif self.regex(stmt, self.move):
				param = self.getParamsAsString(stmt)			#hämtar substrängen mellan parenteserna
				eval("self.move({0})".format(param))
			
			elif self.regex(stmt, self.turnCW):
				param = self.getParamsAsString(stmt)
				eval("self.turnCW({0})".format(param))

			elif self.regex(stmt, self.turnCCW):
				param = self.getParamsAsString(stmt)
				eval("self.turnCCW({0})".format(param))

			elif self.regex(stmt, self.put):
				param = self.getParamsAsString(stmt)
				eval("self.put({0})".format(param))

			elif self.regex(stmt, self.forLoop):
				pass

			else print self.unknownCommand(stmt) 
			
	def forLoop(self, x, to, *stmts):
		pass
	
	def getParamsAsString(self, stmt):
		return stmt[stmt.find("(")+1 : stmt.rfind(")")]		#returnerar substrängen mellan parenteserna
	
	def move(self, steps, angle):
		pass
		
	def moveBackward(self):
		pass
		
	def moveForward(self):
		pass
	
	def penDown(self):
		pen_down = True
	
	def penUp(self):
		pen_down = False
			
	def put(self, xpos, ypos, angle):
		pass
	
	def regex(self, stmt, method):
		return True
	
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
