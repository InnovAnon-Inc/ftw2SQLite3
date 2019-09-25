#! /bin/bash
set -exo nounset

V=-v

OD=$1
shift

ID=$*

[ ! -d "$OD/in.d" ] || \
rm -fr       "$OD/in.d"
mkdir $V     "$OD/in.d"
nice -n -20 \
./extract.sh "$OD/in.d" $ID

nice -n -20 \
python3 ftw2sqlite3.py $V "$OD/db.0"   "$OD/in.d"

nice -n +20 \
rm -rf "$OD/in.d" &

nice -n -20 \
python3 merge1.py      $V "$OD/db.1"   "$OD/db.0"

nice -n +20 \
rm -rf "$OD/db.0" &

nice -n -20 \
python3 merge2.py      $V "$OD/out.db" "$OD/db.1"

nice -n +20 \
rm -rf "$OD/db.1" &

echo 'SELECT password FROM data'  |   \
sqlite3 "$OD/out.db" >   \
        "$OD/train.txt"

( cd ../PassGAN
  nice -n -20       \
  python3 train.py  \
  	--output-dir    "$OD/gann.d"   \
  	--training-data "$OD/train.txt" )

nice -n +20 \
rm -rf "$OD/train.txt" &

( cd ../PassGAN
  nice -n -20       \
  python3 sample.py \
  	--input-dir     "$OD/gann.d"   \
  	--output        "$OD/gann.txt" \
  	--batch-size    1024                        \
  	--num-samples   6000000 )

wait < <(jobs -p)
