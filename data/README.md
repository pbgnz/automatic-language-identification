## corpora

The corpora used for this project were:

1- english
- moby dick
- the little prince

2- french
- le petit prince
- vingt-mile lieues sous les mers

3- spanish
 - don quijote (https://www.gutenberg.org/files/57448/57448-0.txt)
 - la divina comedia (https://www.gutenberg.org/cache/epub/57303/pg57303.txt)

## unix text processing

read text file
```bashrc
less en-moby-dick.txt | less
```

extract words in the corpus
```bashrc
tr -sc 'A-Za-z' '\n' < en-moby-dick.txt | less
```

extract words in the corpus and sort the words alphabetically
```bashrc
tr -sc 'A-Za-z' '\n' < en-moby-dick.txt | sort | uniq -c | less
```

extract words in the corpus and sort the words by frequency
```bashrc
tr -sc 'A-Za-z' '\n' < en-moby-dick.txt | sort | uniq -c | sort -n -r | less
```

same as above but maps upper case letters to lower case
```bashrc
tr 'A-Z' 'a-z' <  en-moby-dick.txt | tr -sc 'A-Za-z' '\n' | sort | uniq -c | sort -n -r | less
```

grep words in the corpus and sort the words by frequency
```bashrc
tr 'A-Z' 'a-z' <  en-moby-dick.txt | tr -sc 'A-Za-z' '\n' | grep '[aeiou].*ing$'| sort | uniq -c | sort -n -r | less
```
