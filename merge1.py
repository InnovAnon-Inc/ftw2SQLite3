from argparse        import ArgumentParser, REMAINDER
from multiprocessing import cpu_count
from oswalk          import oswalk_flattens
from pathlib         import Path
from queue           import Queue
from sqlite3         import connect
from threading       import Thread

from pwformat import PWFormat

class Merge1(Thread):
	def __init__(self, q, outfile):
		Thread.__init__(self)
		self.q       = q
		self.outfile = outfile

		path = Path(outfile)
		if path.exists(): path.unlink()
		path.touch()
	# override
	def run(self):
		q = self.q

		with connect(str(self.outfile)) as outconn:
			outcur = outconn.cursor()
			outcur.execute(PWFormat().create)

			while True:
				infile = q.get()
				if infile is None: break
				self.do_work(infile, outconn, outcur)
				q.task_done()

			outconn.commit()
	def do_work(self, infile, outconn, outcur):
		#with connect(infile) as inconn:
		#	incur = inconn.cursor()
		outcur.execute('''ATTACH ? as indb''', (infile, ))
		outcur.execute('''BEGIN''')
		outcur.execute('''INSERT INTO data SELECT * FROM indb.data''')
		outconn.commit()
		outcur.execute('''DETACH database indb''')
		#	inconn.commit()

if __name__ == "__main__":
	parser = ArgumentParser(
                description='Merge SQLite3 databases into fewer databases'
	)
	#parser.add_argument("-v", "--verbosity", action="count", default=0)
	parser.add_argument('output',                                                help="SQLite3 database(s) output directory")
	parser.add_argument('input', nargs=REMAINDER,                                help="input directory")
	args = parser.parse_args()

	input_dirs = args.input
	output_dir = Path(args.output)
	if not output_dir.exists(): output_dir.mkdir(parents=True)

	q = Queue()

	db_procs = cpu_count()
	threads = [Merge1(q, output_dir.joinpath('tmp-%s.db' % x)) for x in range(db_procs)]

	for t in threads: t.start()
	for file in oswalk_flattens(input_dirs): q.put(file) # enqueue databases to be merged
	q.join()                                             # block until all tasks are done
	for x in range(db_procs): q.put(None)                # stop workers
	for t in threads: t.join()

	# TODO merge threads.outfile
