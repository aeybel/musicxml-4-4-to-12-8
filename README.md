# 4/4 to 12/8 Converter

Oops! Have you ever written a piece of music thinking it was in 4/4 but then it turns out to be in 12/8? This script can help you convert from 4/4 to 12/8!

This script runs on the musicxml format and return a musicxml.

This is a very rudimentary script and is not robust! It works for simple files but if you have a large amount of funky stuff going on, it might lead to unexpected results! Make sure to check over your result file after it has been exported.

Once you export, the rhythm spellings may also be funky. You can use the regroup rhythms function in Musescore to fix this easily. Although sometimes it gets the rules wrong too :(

I have only tested this using Musescore 4 to create, export and import the musicxml files. No guarantees that it would work with imports/exports with other sheet music programs.

P.S. Don't you wish they used a JSON-like format instead of XML? Me too...

## How to Run
Run the following command in the directory with convert.py:
```
py .\convert.py [file-to-process]
```
The resulting musicxml file will be stored in out.musicxml

## The Rules:
Single notes get converted into dotted notes of the same type
> Add a `<dot/>` element after a plain note 

Notes inside a tuple just get the tuple around it removed. Pray that you only have 3-tuples (or their multiples).
> The `<time-modification>` element and its children must be removed.
> The `<notations><tuplet>` element must be removed.

**NOTE:** This program does not convert dotted notes properly. They should be manually converted to tied notes before conversion.

Ties, and other score elements can stay.
