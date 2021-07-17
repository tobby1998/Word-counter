this code is based on the previous work from https://github.com/rocketk/wordcounter. With the code from that, I have add the compatibility of Germen language.

# wordcounter
to count germen words frequency in a text file with nltk
Wörte-Frequenz rechnen

# requirs
- python 3.x
- nltk(to run it properly, maybe you will need the files in "ntlk_data")

# how to use
1. put your text file into the path `wordcounter`, for example, a file named "sophiesworld_1_to_2.txt"
2. execute the following commands
```
cd wordcounter
python word_counter.py
```
3. the result will be writen in the file named `result.txt`

# weitere Optimierung
1 Verbesserung bei der Verarbeitung von verschiedenen Abkürzung, wie z.B. u.a.
2 Mit einem Text einen Stopwordlist automatisch herrzustellen. So kann man nur die Fremdwörter von bestimmtem Text ausziehen.
