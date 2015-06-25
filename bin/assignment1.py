# -*- coding: cp1252 -*-
import JythonTranslater
import re
import math

class program(JythonTranslater.Jtrans):
	
	REGEX_PEN_DOWN 		= "\s*pen down\s*$"
	REGEX_PEN_UP		= "\s*pen up\s*$"
	REGEX_MOVE_FORWARD	= "\s*move forward\s*$"
	REGEX_MOVE_BACKWARD	= "\s*move backward\s*$"
	REGEX_MOVE			= "\s*move\(\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*,\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*\)\s*$"
	REGEX_TURN_CW		= "\s*turn cw\(\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*\)\s*$"
	REGEX_TURN_CCW		= "\s*turn ccw\(\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*\)\s*$"
	REGEX_PUT			= "\s*put\(\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*,\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*,\s*((0|([1-9]\d*))|[a-z])(\s*[+\-*]\s*((0|([1-9]\d*))|[a-z]))*\s*\)\s*$"
	REGEX_FOR			= "\s*for\s+[a-zA-Z]+\s*=\s*(0|([1-9]\d*))\s+to\s+(0|([1-9]\d*))\s+do\s*$"
	
	pen_down = True

	pen_pos_x = 0
	pen_pos_y = 0
	pen_angle = 0

	setPixels = []
		
	def actionPerformed(self, event):
		self.reset()
		code = self.dypl.getCode()
		stmts = code.split("\n") 
		self.doStatements(stmts)
	
	def doStatements(self, stmts):
		index = 0
		
		while index < len(stmts):
			stmt = stmts[index].strip()
			
			# the default number of statements that is evaluated is one per iteration in the while loop, 
			# but a for loop can consist of several statements, so this variable will be used to count 
			# how many, so that we can skip those statements in the next iteration when the for loop has ended.
			stmtCount = 1	
			
			if re.match(self.REGEX_FOR, stmt):
				# the forLoop method will execute all statements from the current position to the
				# end as long as it doesn't reach an 'end' statement
				stmtCount = self.forLoop(stmt, stmts[index + 1:])
			elif stmt == "":
				pass
			else:
				try:	
					eval(self.get_stmt(stmt))
				except:
					#raise
					print stmt, " is an unknown command"
					return
				
			index += stmtCount
	
	def get_stmt(self, stmt):
		if not re.match("[a-z]*\(", stmt):
			stmt = stmt.replace(" ", "_")
		
		# if "pen_down", "pen_up", "move_forward" or "move_backward", add parentheses to be able to call method
		if not re.match(".*\(", stmt):
			stmt += "()"
		
		return "self." + stmt
	
	def forLoop(self, stmt, stmts):
		# gets the variable name
		var_name = re.search("[a-zA-Z]+\s*=", stmt).group().strip(" =")

		# gets the variable value
		var_value = int(re.search("=\s*(0|([1-9]\d*))", stmt).group().strip("= "))
		
		# gets target value
		target = int(re.search("to\s*(0|([1-9]\d*))", stmt).group().strip("to "))
				
		for index in xrange(var_value, target):
			stmtCount = 1  		# reset because it's the inner for loop that will do the counting
			
			for stmt in stmts:
				stmtCount += 1
				
				if stmt == "end":
					break
				
				stmt = stmt.replace(var_name, str(index))
				eval(self.get_stmt(stmt))
				
		return stmtCount
	
	def move(self, steps, angle):
		self.pen_angle += angle
		
		if steps < 1: return
		
		delta_x = math.cos(math.radians(self.pen_angle-90))
		delta_y = math.sin(math.radians(self.pen_angle-90))
		
		if self.pen_down:
			positions_x = map(lambda x: self.pen_pos_x + x * delta_x, range(steps))
			positions_y = map(lambda y: self.pen_pos_y + y * delta_y, range(steps))
			
			for i in xrange(steps):
				x = int(positions_x[i])
				y = int(positions_y[i])
				self.dypl.setPixel(x, y)
				self.setPixels.append((x, y))
			
		self.pen_pos_x += steps * delta_x
		self.pen_pos_y += steps * delta_y
		
	def move_backward(self):
		self.move(1, 180)
		self.turnCW(180)
		
	def move_forward(self):
		self.move(1, 0)
	
	def pen_down(self):
		self.pen_down = True
		
	def pen_up(self):
		self.pen_down = False

	def put(self, xpos, ypos, angle):
		self.pen_pos_x = xpos
		self.pen_pos_y = ypos
		self.pen_angle = angle		
	
	def reset(self):
		for e in self.setPixels:
			self.dypl.unsetPixel(*e)
			
		self.pen_pos_x = self.pen_pos_y = self.pen_angle = 0
	
	def setDYPL( self, obj ):
		self.dypl = obj
	
	def turn_cw(self, angle):
		self.pen_angle += angle
		
	def turn_ccw(self, angle):
		self.pen_angle -= angle
		
if __name__ == '__main__':
    import DYPL
    DYPL(program())
