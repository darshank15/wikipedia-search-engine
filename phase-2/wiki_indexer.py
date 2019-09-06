#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import operator
from math import *
from heapq import *
from include1 import *
from collections import *
import os
import time
import xml.etree.cElementTree as et
import re
import sys


wiki_path  = sys.argv[1]
index_path = sys.argv[2]

start = time.time()

output_files = list()
title_position = list()
word_position = dict()

# Defaut list of title,text,infobox,output_index.........inverted index

title_index = defaultdict(list)
text_index = defaultdict(list)
category_index = defaultdict(list)
infobox_index = defaultdict(list)


# RE to remove urls
regExp1 = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',re.DOTALL)
# RE to remove tags & css
regExp2 = re.compile(r'{\|(.*?)\|}',re.DOTALL)


page_count = 0 # denote which number of wiki page it is

# if not os.path.exists():
#     os.makedirs(my_path+"/files")


xmlFile = wiki_path
#any tag start end
context = et.iterparse(xmlFile, events=("start", "end"))
context = iter(context)
title_tags = open(index_path+"/title_tags.txt", "w+")


def preprocee_word(word) :

    word = word.strip()
    word = word.lower() # convert into lower case
    word = stemmer.stem(word) # do stemming
    return word

for event, elem in context :
    tag =  re.sub(r"{.*}", "", elem.tag)

    if event == "start" :
        if tag == "page" :
            page_count += 1
            title_tag_words =  dict()
            category_words =  dict()
            infobox_words =  dict()
            text_tag_words =  dict()
           
    if event == "end" :
        
        if tag == "text" :
            text = str(elem.text)
            text = regExp1.sub('',text)
            text = regExp2.sub('',text)
            
            try :
                tempword = re.findall("\[\[Category:(.*?)\]\]", text); # get all data between [[Category : ----- ]]
                if tempword :
                    for temp in tempword :
                        temp = re.split(pattern, temp);#print(pattern)
                        for t in temp :
                            t = preprocee_word(t)
                            if t :
                                if len(t) <= 2 :
                                    continue
                                if  t not in stop_words :
                                    if t not in category_words:
                                        category_words[t] = 1
                                    else : 
                                        category_words[t] += 1

                tempword = re.findall("{{Infobox((.|\n)*?)}}", text) # get all data between infobox{{ ----- }}
                if tempword :
                    for temp in tempword :
                        for word in temp : 
                            temp = re.split(pattern, word);#print(pattern)
                            for t in temp :
                                t = preprocee_word(t)
                                if t :
                                    if len(t) <= 2 :
                                        continue
                                    if  t not in stop_words :
                                        if t not in infobox_words :
                                            infobox_words[t] = 1
                                        else :
                                            infobox_words[t] += 1
            except :
                pass

            try :
                text = text.lower();
                text = re.split(pattern, text);

                for word in text :
                    if word :
                        word = stemmer.stem(word)
                        if word not in stop_words :
                            if len(word) <= 2 :
                                    continue
                            if word not in text_tag_words :
                                text_tag_words[word] = 1
                            else :
                                text_tag_words[word] += 1

            except :
                pass     
        if tag == "title" :
            text = elem.text;
            try :
                title_string = text + "\n"
                text = text.lower();
#                 title tag file mei yeh title kis position pe add
                title_position.append(title_tags.tell())
                title_tags.write(title_string)
                text = re.split(pattern, text);

                for word in text :
                    if word :
                        word = stemmer.stem(word)
                        if word not in stop_words :
                            if len(word) <= 2 :
                                continue
                            if word not in title_tag_words :
                                title_tag_words[word] = 1
                            else :
                                title_tag_words[word] += 1

            except :
                pass

        # Posting list start
        if tag == "page" :

            index = str(page_count) # get document ID ==> Wiki page number
            for word in text_tag_words :
                s = index + ":" + str(text_tag_words[word]);
                text_index[word].append(s)

            for word in title_tag_words :
                s = index + ":" + str(title_tag_words[word])
                title_index[word].append(s)

            for word in category_words :
                s = index + ":" + str(category_words[word])
                category_index[word].append(s)

            for word in infobox_words :
                s = index + ":" + str(infobox_words[word])
                infobox_index[word].append(s)


        elem.clear()


# In[8]:


file = open(index_path+"/title_positions.pickle", "wb+")
pickle.dump(title_position, file)
file.close()


# In[9]:


word_position = dict() # store word & its occurence/file pointer in title file, infobox file, body file
# abc word : { { t : fpt1_val}, { b : fpt2_val}, { c : fpt3_val}, { b : fpt4_val} }

fptr=0
file = index_path + "/t_1.txt"
outfile = open(file, "w+")
for word in title_index:
    index = ",".join(title_index[word])
    index = index+"\n"
    outfile.write(index)
    if word not in word_position :
        word_position[word] = {}
    word_position[word]['t']=fptr
    fptr = fptr + len(index)
outfile.close();

fptr=0
file = index_path + "/b_1.txt"
outfile = open(file, "w+")
for word in text_index :
    index = ",".join(text_index[word])
    index = index+"\n"
    if word not in word_position:
        word_position[word] = {}
    word_position[word]['b']=fptr
    outfile.write(index)
    fptr = fptr + len(index)
outfile.close()

fptr=0
file = index_path + "/c_1.txt"
outfile = open(file, "w+")
for word in category_index :
    index = ",".join(category_index[word])
    index = index+"\n"
    if word not in word_position:
        word_position[word] = {}
    word_position[word]['c']=fptr
    outfile.write(index)
    fptr = fptr + len(index)
outfile.close()

fptr=0
file = index_path + "/i_1.txt"
outfile = open(file, "w+")
for word in infobox_index:
    index = ",".join(infobox_index[word])
    index = index+"\n"
    if word not in word_position:
        word_position[word] = {}
    word_position[word]['i']=fptr
    outfile.write(index)
    fptr = fptr + len(index)
outfile.close()


# In[10]:


file = open(index_path+"/word_positions.pickle", "wb+")
pickle.dump(word_position, file)
file.close()

end = time.time()
# print("Time taken - " + str(end - start) + " s")


# In[ ]:


# print(word_position)

