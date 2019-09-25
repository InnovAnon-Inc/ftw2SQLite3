from abc import ABCMeta
from abc import abstractmethod
from re  import compile

class Format(metaclass=ABCMeta):
	def __init__ (self, regex, n, create, insert):
		self.prog   = compile(regex)
		self.n      = n
		self.create = create
		self.insert = insert
	@abstractmethod
	def parseLine(self, line): raise Error('''abstract method''')
