class Config:
	def __init__(self,
		input_dir, output_dir,
		read_procs, mmap_size):

		self.input_dir        = input_dir
		self.output_dir       = output_dir

		self.read_procs       = read_procs
		self.mmap_size        = mmap_size
