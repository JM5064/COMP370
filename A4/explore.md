## How big is the dataset?

`wc clean_dialog.csv` : `   36860  670166 4870970 clean_dialog.csv`

36860 lines, 670166 words, 4870970 characters


## What’s the structure of the data? (i.e., what are the field and what are values in them)

`head -n 2 clean_dialog.csv`

"title","writer","pony","dialog"
They are all strings, representing the hheads


## How many episodes does it cover?

`wc -l pony_data` -1 = 197


## During the exploration phase, find at least one aspect of the dataset that is unexpected – meaning that it seems like it could create issues for later analysis.

There are multiple different cases of non-spoken text by different authors (Narrator, Other, ...), and sometimes, the Narrator could be cited as a speaker along with a pony. 
