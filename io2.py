from mmap    import ACCESS_READ, mmap
from os      import stat
from sqlite3 import connect

from input   import read_lines
from output  import write_db

def io2(fname, config, format):
	sz = stat(fname).st_size
	if not sz: return

	#try:
	#	lock.acquire()
	#	count = dbcur.execute('''SELECT EXISTS(SELECT 1 FROM data WHERE filename=? LIMIT 1)''', (fname,)).fetchone()
	#	print(str(count) + ": " + fname)
	#	if count[0]: return
	#finally: lock.release()

	with open(fname, 'r+b') as fp:
	#with open(fname, 'r') as fp:
		with mmap(fp.fileno(), min(sz, config.mmap_size), prot=ACCESS_READ) as mf:
			def bar(cur, line):
				#params = prog.split(line, maxsplit=1)
				params = format.parseLine(line)
				if len(params) is format.n:
					#cur.execute("INSERT INTO data VALUES (?, ?)", params)
					cur.execute(format.insert, params)
				else:
					# TODO record error
					pass
				#print(line)
			def foo(cur):
				#cur.execute('''CREATE TABLE data (user text, password text)''')
				cur.execute(format.create)
				read_lines(mf, lambda line: bar(cur, line))
				
			print(fname)
			db = write_db(fname, config.output_dir, foo)
			print(db)
			#mf.flush()

	#try:
	#	lock.acquire()
	#	dbcur.execute('''INSERT INTO data VALUES (?, ?)''', (fname, db))
	#	dbconn.commit()
	#finally: lock.release()
