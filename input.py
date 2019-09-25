def lines(mf): return iter(mf.readline, b"")
def read_lines(mf, f):
	#map(lambda g: f(str(g)), lines(mf))
	for g in lines(mf):
		#f(str(g))
		f(str(g).strip())
