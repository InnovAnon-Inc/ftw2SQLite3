from os        import path,  stat,    walk
from itertools import chain, starmap

# these should have less memory overhead and better response time,
# meaning you can start enqueuing the work tasks sooner
# meaning you can use more cores sooner

def oswalk_helper(root, dirs, files): return map(lambda name: path.join(root, name), files)
def oswalk(x):                        return starmap(oswalk_helper, x)
def oswalk_flatten(input_dir):        return chain.from_iterable(oswalk(walk(input_dir)))
def oswalk_flattens(input_dirs):      return chain.from_iterable(map(lambda input_dir: oswalk_flatten(input_dir), input_dirs))
def oswalk_nonempty(input_dir):       return filter(lambda fname: stat(fname).st_size, oswalk_flatten(input_dir))
