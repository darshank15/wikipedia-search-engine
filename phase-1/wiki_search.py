#!/usr/bin/env python
# coding: utf-8

# In[16]:


from include1 import *
import operator
import time
import copy
import sys


# In[17]:


def read_file(testfile):
    with open(testfile, 'r') as file:
        queries = file.readlines()
    return queries


# In[18]:


def write_file(outputs, path_to_output):
    '''outputs should be a list of lists.
        len(outputs) = number of queries
        Each element in outputs should be a list of titles corresponding to a particular query.'''
    with open(path_to_output, 'w') as file:
        for output in outputs:
            for line in output:
                file.write(line.strip() + '\n')
            file.write('\n')


# In[19]:


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


# In[20]:


def search(path_to_index, queries):
    
    title_tags = open(path_to_index+"/title_tags.txt", "r")
    title_position = pickle.load(open(path_to_index+"/title_positions.pickle", "rb"))
    word_position = pickle.load(open(path_to_index+"/word_positions.pickle", "rb"))

    field_map = {"t" : 0, "b" : 1, "i" : 2, "c" : 3}
    field_chars = ["t", "b", "i", "c"] 
    files = []

    for f in field_chars :
        file = path_to_index+"/" + f + "_1.txt"
        fp = open(file, "r")
        files.append(fp)
        
    final_result = []
    for query in queries :
        
        # print(query)

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
            intersection=0
            for q in query_bag :
                
                # print("q :",q)
                field, query = q.split(":")
                # field = field.strip()
                field = mapping_shortform(field)
    #             print(field)
    #             print(query)
                query_words = query.split()
                for word in query_words :
                    docs=list()
                    word = stemmer.stem(word)
                    if word in word_position and field in word_position[word] :
                        position = word_position[word][field]
                        files[field_map[field]].seek(position)
                        s = files[field_map[field]].readline()[:-1]
                        temp_docs = s.split(",")
                        for doc in temp_docs : 
                            docs.append(doc.split(":")[0])
                        if intersection==0:
                            intersection = 1
                            t_result=copy.deepcopy(list(set(docs)))
                        else:
                            t_result=copy.deepcopy(list(set(t_result) & set(docs)));

            for item in t_result : 
                result.append(item)

            result = set(result)
            
            # print(len(result))

        else :
            intersection=0    
            query_bag = query.split()      
            length = len(query_bag)
            for i in range(length) :
                query_bag[i] = stemmer.stem(query_bag[i])
            for word in query_bag :
                if word not in stop_words and word in word_position:
                    query_words.append(word)

            for word in query_words :
                docs = list()
                positions = word_position[word]
                for field in positions.keys() :
                    position = positions[field]
                    files[field_map[field]].seek(position)
                    s = files[field_map[field]].readline()[: -1]
                    temp_docs = s.split(",")
                    for doc in temp_docs : 
                        docs.append(doc.split(":")[0])
                if intersection==0:
                    intersection = 1
                    result=copy.deepcopy(list(set(docs)))
                else:
                    result=copy.deepcopy(list(set(result) & set(docs)))

        end = time.time()
        if len(result) == 0 :
            tilte_result = []
#             print("No reults found")
#             print("Time taken - " + str(end - start) + "s")
        else :
#             print("Results retrieved in - " + str(end - start) + "s")
            result= set(result)
            tilte_result = []
#             print("No-",len(result))
            count=1
            for d_id in result:
                pointer=title_position[int(d_id)-1]
                title_tags.seek(pointer)
                title=title_tags.readline()[:-1]
                tilte_result.append(title)
                count = count + 1
                if count > 10 :
                    break
         
        final_result.append(tilte_result)
        # print(len(tilte_result))

    return final_result


# In[21]:


def main():
    path_to_index = sys.argv[1]
    testfile = sys.argv[2]
    path_to_output = sys.argv[3]

    queries = read_file(testfile)
    outputs = search(path_to_index, queries)
    write_file(outputs, path_to_output)


# In[22]:


if __name__ == '__main__':
    main()

