#from mmap            import ACCESS_WRITE, mmap
from os              import sep
from pathlib         import Path
from sqlite3         import connect

def open_tmp2(fname, output_dir, f):
	#  TODO check if exists
	fpath  = Path(fname)
	if not fpath.is_absolute(): fpath = fpath.resolve()
	fpath = fpath.relative_to(sep)
	dbpath = Path(output_dir)
	dbpath = dbpath.joinpath(fpath, '.db')
	parent = dbpath.parent
	if not parent.exists(): parent.mkdir(parents=True)
	db = dbpath
	with open(db, 'w') as tmp:
		f(tmp)
		#with mmap(tmp.fileno(), mmap_size, prot=ACCESS_WRITE) as tmp2:
		#	f(tmp2)
	return db
def open_db(fname, output_dir, f):
	def foo(tmp):
		#with connect(tmp.name) as conn:
		with connect(str(tmp)) as conn:
			# try ?
			f(conn)
			conn.commit()
	return open_tmp2(fname, output_dir, foo)
def write_db_helper(conn, f):
	cur = conn.cursor()
	f(cur)
def write_db(fname, output_dir, f): return open_db(fname, output_dir, lambda cur: write_db_helper(cur, f))
