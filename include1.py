import re
import os
import sys
import pickle
import base64
# from Stemmer import Stemmer
import nltk

stemmer = nltk.stem.SnowballStemmer('english')
pattern = re.compile("[^a-zA-Z0-9]")
stop_words = {}
reg = re.compile("\"|,| ")
stop_file = open("stop_words.txt", "r")
content = stop_file.read()
content = re.split(reg, content)
for word in content :
	if word :
		stop_words[word] = True