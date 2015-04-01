# -*- coding: cp1252 -*-
import JythonTranslater

class program(JythonTranslater.Jtrans):
	
	pen_down = False
	
	pen_pos_x = 0.0
	pen_pos_y = 0.0
	pen_angle = 0
	
	stmtsToLoop = []
	
	def actionPerformed(self, event):
		str = self.dypl.getCode()
		stmts = str.split("\n") 
		self.doStatements(stmts)
	
	def doStatements(self, stmts):
	
		index = 0
		while index < len(stmts):
			stmt = stmts[index]
			if self.regex(stmt, self.penDown): # regex �r en metod som kollar om item matchar regexet f�r penDown etc.
				self.penDown()
				
			elif self.regex(stmt, self.penUp):
				self.penUp()
			
			elif self.regex(stmt, self.moveForward):
				self.moveForward()
				
			elif self.regex(stmt, self.moveBackward):
				self.moveBackward()

			elif self.regex(stmt, self.move):
				param = self.getParamsAsString(stmt)			#h�mtar substr�ngen mellan parenteserna
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
				params = stmt.split(\s*)		#delar upp headern f�r for-loopen
				var_name = params[1]			#variabelnamnet h�mtas
				var = int(params[3])			#variabelns v�rde h�mtas
				target = int(params[6])			#m�let p� loopen h�mtas
				
				try:
					endOfLoop = stmts.index("end",index) #h�mtar radnumret d�r loopen slutar

				except ValueError:
					print "for-loop without 'end'"		#om det inte finns ett "end" s� skickas ett felmeddelande och metoden avbryts
					break
				
				self.forLoop(var_name, var, target, stmts[index:endOfLoop] #alla rader mellan d�r vi st�r och "end" skickas
				index = endOfLoop 										#vi st�ller oss p� index f�r "end"
			else:
				print self.unknownCommand(stmt)
			
			++index
	
	def forLoop(self, var_name, value, to, *stmts):
		new_statements = stmts[:]					#copies stmts
		for index in xrange(value, to):				#executes all statements the requested # of times			
			for index2 in xrange(len(stmts)):			#replaces all variables with a value
				new_statements[index2] = stmts[index2].replace(var_name, index)
			
			self.doStatements(new_statements)
	
	def getParamsAsString(self, stmt):
		return stmt[stmt.find("(")+1 : stmt.rfind(")")]		#returnerar substr�ngen mellan parenteserna
	
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
