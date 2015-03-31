import JythonTranslater

class program(JythonTranslater.Jtrans):
	
	pen_down = False
	
	pen_pos_x = 0.0
	pen_pos_y = 0.0
	pen_angle = 0
	
	methods = {
		"move"			: move,
		"move backward" : moveBackward,
		"move forward" 	: moveForward,
		"pen down" 		: penDown,
		"pen up" 		: penUp,
		"turn cw" 		: turnCW,
		"turn ccw"		: turnCCW,
		"put"			: put,
		"for"			: forLoop}
		
	eval(methods["move"] + "(steps, angle)") # move(steps, angle)
	def actionPerformed(self, event):
		str = self.dypl.getCode()
		str = str.split("\n")
		for line in str:
			pass
			
	def forLoop(x, to, *stmts)
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