from format import Format

class PWFormat(Format):
	def __init__(self):
		Format.__init__(self,
			"[:;|]", 2,
			'''CREATE TABLE data (user text, password text)''',
			'''INSERT INTO data VALUES (?, ?)''')
	def parseLine(self, line): return self.prog.split(line, maxsplit=self.n)
