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
			if self.regex(stmt, self.penDown): # regex �r en metod som kollar om item matchar regexet f�r penDown etc.
				self.penDown()
			elif self.regex(stmt, self.move):
				# tar bort ( och ) s� bara argumenten blir kvar och l�gger
				# in i move(...)
				param = stmt[stmt.find("(")+1:stmt.rfind(")")]		#h�mtar substr�ngen mellan parenteserna
				eval("self.move({0})".format(param))
                 #       [...]
                  #      elif [...]
                   #     else:
                    #         print "invalid input"   
			
	def forLoop(self, x, to, *stmts):
		pass
		
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
