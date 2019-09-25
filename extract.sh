#! /bin/bash
set -exo nounset

ID=$1
shift

cd "$ID"
find $* \
  	\( \( -iname \*.gz    -o \
  	      -iname \*.gzip  -o \
	      -iname \*.tgz   -o \
	      -iname \*.z     -o \
	      -iname \*-z     -o \
	      -iname \*_z     \) \
  	-exec tar xI pigz   -f '{}' \; \) -o \
  	\( \( -iname \*.bz    -o \
	      -iname \*.bzip2 -o \
	      -iname \*.tbz   -o \
	      -iname \*.bz2   -o \
	      -iname \*.tbz2  \) \
	-exec tar xI pbzip2 -f '{}' \; \) -o \
	\( \( -iname \*.lz    -o \
	      -iname \*.tlz   -o \
	      -iname \*.lzip  \) \
	-exec tar xI plzip  -f '{}' \; \) -o \
	\( \( -iname \*.xz    -o \
	      -iname \*.txz   -o \
	      -iname \*.xzip  -o \
	      -iname \*.lzma  \) \
	-exec tar xI pixz   -f '{}' \; \) -o \
	-print       | \
xargs -P`nproc` -I %   \
tar xf %               \
2> /dev/null
