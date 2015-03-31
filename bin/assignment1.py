import JythonTranslater
class program(JythonTranslater.Jtrans):
	
	def actionPerformed(self, event):
		str = self.dypl.getCode()
		str = str.split("\n")
		for s in str:
			print s.strip()

	def setDYPL( self, obj ):
		self.dypl = obj
	
if __name__ == '__main__':
    import DYPL
    DYPL(program())