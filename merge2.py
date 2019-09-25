from argparse        import ArgumentParser, REMAINDER
from multiprocessing import cpu_count
from oswalk          import oswalk_flattens
from pathlib         import Path
from sqlite3         import connect

from pwformat import PWFormat
from oswalk   import oswalk_flatten

if __name__ == "__main__":
	parser = ArgumentParser(
                description='Merge SQLite3 databases into fewer databases'
	)
	#parser.add_argument("-v", "--verbosity", action="count", default=0)
	parser.add_argument('output', help="SQLite3 database output")
	parser.add_argument('input',  help="SQLite3 database input directory")
	args = parser.parse_args()

	input_dir = Path(args.input)
	output    = Path(args.output)
	if output.exists(): output.unlink()
	output.touch()

	with connect(str(output)) as outconn:
		outcur = outconn.cursor()
		outcur.execute(PWFormat().create)

		for infile in oswalk_flatten(input_dir):
			outcur.execute('''ATTACH ? as indb''', (str(infile), ))
			outcur.execute('''BEGIN''')
			outcur.execute('''INSERT INTO data SELECT * FROM indb.data''')
			outconn.commit()
			outcur.execute('''DETACH database indb''')
		
		outconn.commit()
