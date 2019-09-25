from argparse        import ArgumentParser, REMAINDER
from importlib       import import_module
from multiprocessing import Pool,           cpu_count
from psutil          import virtual_memory

from config          import Config
from io2             import io2
from oswalk          import oswalk_flattens

if __name__ == "__main__":

	parser = ArgumentParser(description='File Tree Walk convert files to SQLite3.')
	#parser.add_argument("-v", "--verbosity", action="count", default=0)
	parser.add_argument('-m', '--format_module',             default="pwformat", help="Python module containing Format implementation subclass")
	parser.add_argument('-c', '--format_class',              default="PWFormat", help="Python Format implementation subclass")
	parser.add_argument('output',                                                help="SQLite3 database(s) output directory")
	parser.add_argument('input', nargs=REMAINDER,                                help="input directory")
	args = parser.parse_args()

	input_dir  = args.input
	output_dir = args.output

	available_memory = virtual_memory().available
	read_procs       = cpu_count()
	mmap_size        = available_memory // read_procs

	config = Config(input_dir, output_dir, read_procs, mmap_size)

	module_name = args.format_module
	class_name  = args.format_class

	module = import_module(module_name)
	class_ = getattr(module, class_name)
	format = class_()

	p = Pool(processes=read_procs)
	p.starmap(io2, map(lambda x: (x, config, format), oswalk_flattens(input_dir)))
