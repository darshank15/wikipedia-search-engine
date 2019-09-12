#!/usr/bin/env python
# coding: utf-8

# In[28]:


import operator
import time
import copy
import sys
import gc
import json
import os
import re
import sys
import pickle
import base64
import nltk   
import json


# In[29]:


# title_position = pickle.load(open("/home/darshan/Documents/M.Tech_SEM-3/IRE/projects/mini-projects/wikipedia-search-engine/phase-2/files/title_positions.pickle", "rb"))


# In[30]:


# word_position = pickle.load(open("/home/darshan/Documents/M.Tech_SEM-3/IRE/projects/mini-projects/wikipedia-search-engine/phase-2/files/word_positions.pickle", "rb"))


# In[31]:


def read_file(testfile):
    with open(testfile, 'r') as file:
        queries = file.readlines()
    return queries


# In[32]:


def write_file(outputs, path_to_output):
    '''outputs should be a list of lists.
        len(outputs) = number of queries
        Each element in outputs should be a list of titles corresponding to a particular query.'''
    with open(path_to_output, 'w') as file:
        for output in outputs:
            for line in output:
                file.write(line.strip() + '\n')
            file.write('\n')


# In[33]:


def mapping_shortform(field) :
    
    field = field.lower()
    
    if field == "title" :
        return "t"
    elif field == "infobox" :
        return "i"
    elif field == "category" :
        return "c"
    elif field == "body" :
        return "b"
    elif field == "ref" :
        return "b"
    else :
        return field


# In[34]:


def search(path_to_index):
    
    stemmer = nltk.stem.SnowballStemmer('english')

    stop_words = {}
    reg = re.compile("\"|,| ")
    stop_file = open("stop_words.txt", "r")
    content = stop_file.read()
    content = re.split(reg, content)
    for word in content :
        if word :
            stop_words[word] = True
            
    title_tags = open(path_to_index+"/title_tags.txt", "r")
    title_position = pickle.load(open(path_to_index+"/title_positions.pickle", "rb"))
    word_position = pickle.load(open(path_to_index+"/word_positions.pickle", "rb"))

    field_map = {"t" : 0, "b" : 1, "i" : 2, "c" : 3}
    field_chars = ["t", "b", "i", "c"] 
    files = []

    for f in field_chars :
        file = path_to_index+ "/" + f + ".txt"
        fp = open(file, "r")
        files.append(fp)
        
#     final_result = []
    while(1) :
        
        query = input()
        # print(query)
        start = time.time()
        result = []
        documents = dict()
        query_words = list()

        # query = query.lower().strip()
#         start = time.time()
#         if (query == "exit") :
#             break

        if ":" in query :
            query_bag = query.split(" ")
            t_result=list()
            flag2=0
            for q in query_bag :
                field_query = q.split(":")
                field = field_query[0]
                query = field_query[1]
                field = mapping_shortform(field)
                query_words = query.split()
                for word in query_words :
                    word = stemmer.stem(word)
                    if word in word_position and field in word_position[word] :
                        position = word_position[word][field]
                        files[field_map[field]].seek(position)
                        intersection=list()
                        s = files[field_map[field]].readline()[:-1] # remove "/n" [:-1] & read full line of posting list
                        if "," in s :
                            items = s.split(",")
                            for item in items :
                                document_score = item.split(":")
                                doc_id = document_score[0]
                                score = document_score[1]
                                tt = 1
                                if doc_id in documents :
                                    documents[doc_id] = documents[doc_id] + float(score)
                                else :
                                    documents[doc_id] = float(score)
                        else :
                            document_score = item.split(":")
                            doc_id = document_score[0]
                            score = document_score[1]
                            tt = 1
                            union_list = list()
                            if doc_id in documents :
                                documents[doc_id] = documents[doc_id] + float(score)
                            else :
                                documents[doc_id] = float(score)
                        

        else :    
            query_bag = query.split()      
            length = len(query_bag)
            for i in range(length) :
                query_bag[i] = stemmer.stem(query_bag[i])
                
            for word in query_bag :
                if word not in stop_words and word in word_position:
                    query_words.append(word)

            for word in query_words :
                docs = list()
                flag2=0
                positions = word_position[word]
                for field in positions.keys() :
                    position = positions[field]
                    intersection=list()
                    files[field_map[field]].seek(position)
                    s = files[field_map[field]].readline()[: -1]
                    if "," in s :
                        items = s.split(",")
                        for item in items :
                            document_score = item.split(":")
                            doc_id = document_score[0]
                            score = document_score[1]
                            tt = 1
                            if doc_id in documents :
                                documents[doc_id] =  documents[doc_id] + float(score)
                            else :
                                documents[doc_id] = float(score)
                                
                    else :
                        document_score = item.split(":")
                        doc_id = document_score[0]
                        score = document_score[1]
                        tt = 1
                        union_list = list()
                        if doc_id in documents :
                            documents[doc_id] =  documents[doc_id] + float(score)
                        else:
                            documents[doc_id] = float(score)
        
        documents = sorted(documents.items(), key = operator.itemgetter(1), reverse = True)
        count = 1
        end = time.time()
        print("Response Time :  " + str(end - start) + " s\n")
        for document in documents :
            
            position = title_position[int(document[0]) - 1]
            title_tags.seek(position)
            title = title_tags.readline()[: -1]
            result.append(title)
            print(title)
            count += 1
            if count > 10 :
                    break
        
        print("\n")
        
#         final_result.append(result)
        # print(len(tilte_result))

#     return final_result


# In[35]:


def main():
    
    path_to_index = sys.argv[1]
#     testfile = sys.argv[2]
#     path_to_output = sys.argv[3]

#     path_to_index = "/home/darshan/Documents/M.Tech_SEM-3/IRE/projects/mini-projects/wikipedia-search-engine/phase-2/files"
#     testfile = "/home/darshan/Documents/M.Tech_SEM-3/IRE/projects/mini-projects/wikipedia-search-engine/phase-2/input/queryfile"
#     path_to_output = "/home/darshan/Documents/M.Tech_SEM-3/IRE/projects/mini-projects/wikipedia-search-engine/phase-2/output/result"

#     queries = read_file(testfile)
    search(path_to_index)
#     write_file(outputs, path_to_output)


# In[36]:


if __name__ == '__main__':
    main()


# In[ ]:





# In[ ]:




