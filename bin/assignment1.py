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
			if regex(stmt, penDown): # regex är en metod som kollar om item matchar regexet för penDown etc.
				penDown()
			elif regex(stmt, move):
				# tar bort ( och ) så bara argumenten blir kvar och lägger
				# in i move(...)
				param = stmt[stmt.find("("):stmt.rfind(")")]
				print param
				#eval("move({0})".format(stmt.strip("(").strip(")")))
                 #       [...]
                  #      elif [...]
                   #     else:
                    #         print "invalid input"   
			
	def forLoop(x, to, *stmts):
		pass
		
	def move(steps, angle):
		pass
		
	def moveBackward():
		pass
		
	def moveForward():
		pass
	
	def penDown():
		pen_down = True
	
	def penUp():
		pen_down = False
			
	def put(xpos, ypos, angle):
		pass
		
	def setDYPL( self, obj ):
		self.dypl = obj
	
	def turnCW(angle):
		pass
		
	def turnCCW(angle):
		pass
		
	def unknownCommand(str):
		print str, " is an unknown command"
		
if __name__ == '__main__':
    import DYPL
    DYPL(program())
