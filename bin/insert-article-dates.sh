#! /bin/bash

# This changes IFS so that we can handle spaces in file names
OIFS="$IFS"
IFS=$'\n'

for f in `find . -type f -name "*.markdown"`;
  # Script which inserts the first commit date into a 'date' meta field in each article.
  do git log --format=%ci --diff-filter=A $f | cut -d ' ' -f 1 | xargs echo $f # -I ARG -- sed -i '5i date: "ARG"' $f ;
done

# Restore IFS
IFS="$OIFS"
