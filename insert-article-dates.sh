for f in `ls docs/articles/*.markdown`;
  # Script which inserts the first commit date into a 'date' meta field in each article.
  do git log --format=%ci $f | tail -n 1 | egrep -o '[0-9\-]{5,}' | xargs -I ARG -- sed '5i date: "ARG"' $f ;
done
