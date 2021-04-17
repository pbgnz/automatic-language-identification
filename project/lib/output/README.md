## output

The program outputs:

1. a dump of the language models in the following files:
- unigramFR.txt, bigramFR.txt, unigramEN.txt, bigramEN.txt, unigramOT.txt, bigramOT.txt

2. For each input sentence in the input (test) file:
- a. on the console, the most probable language of the sentence
- b. a dump of the trace of that sentence in a file name out#.txt where # is the number of the sentence 
    in the input file.
    Each output file must contain the sentence itself, a trace and the result of its classification, following
    the format below.
    For example, if the input file contains 30 sentences to test, then you should generate 30 output files
    named out1.txt to out30.txt .
