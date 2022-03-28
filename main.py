#TEAM MEMBERS
#Saransh Dwivedi - 2019A7PS0173H
#Shantanu Kumar - 2019B3A70375H
#Gokul Pradeep - 2018B5A70785H

import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import time
dict = {}
files ={}
file_no = 1
directory = 'Documents'
stop_words = set(stopwords.words('english'))  #stop_words contains all english stop words
ps = PorterStemmer()

## iterate over files in the given directory ##
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        with open(f,'r') as file:
            # adding file num and name to dictionary files
            files[file_no] = filename             
            # reading each line    
            for line in file:
                word_tokens = word_tokenize(line)
                # reading each word        
                for word in word_tokens:
                    #adding the stemmed word
                    word = ps.stem(word) 
                    if word not in stop_words:
                        if word in dict:
                            if dict[word][-1] != filename: 
                                dict[word].append(filename)
                        else:
                            dict[word]=[filename]
            file_no += 1  

########## boolean query ##########

## or operatin  ##
def or_ope(a,b):
    """OR operation finds the union of two lists"""
    or_list = list(set(a) | set(b))
    or_list.sort()
    return or_list

## and operation ##
def and_ope(a,b):
    """AND operation finds the intersection of two lists"""
    and_list = list(set(a) & set(b))
    and_list.sort()
    return and_list
## not operation ##
def not_ope(a):
    """NOT operation returns all documents where the word is not present """
    not_list = []
    j=0
    for i in files:
        not_list.append(files[i]) 
    return list(set(not_list)-set(a))

operator = []
operand = [] 

## identifies if the token is an operator or an operand ##
def bool_query(s):
    """This function identifies if the token is an operator or an operand"""
    query_token = word_tokenize(s)
    for word in query_token:
        if word == ("AND") or word ==("OR") or word ==("NOT") or word ==("("):
            operator.append(word)
        elif word ==(")"):
            calculate(operator,operand)
        else:
            word = check_word(ps.stem(word))  ## checks if the word is peresent in our dictionary 
            operand.append(dict[word])
    calculate(operator,operand)

## AND, OR and NOT functions are called ##
def calculate(operator,operand):  
    """This function calls AND, OR and NOT functions"""
    while(len(operator) != 0):
        st_top = ""
        st_top = operator.pop()
        if(st_top == "and" or st_top == "AND"):
            operand.append(and_ope(operand.pop(),operand.pop()))
        elif(st_top == "or" or st_top == "OR"):
            operand.append(or_ope(operand.pop(),operand.pop()))
        elif(st_top == "not" or st_top =="NOT"):
            operand.append(not_ope(operand.pop()))
        elif(st_top == "("):
            break

## check is the word is present in or dictionary ##
## if not class the edit_distance ##
def check_word(word):
    """Checks if the word is present in the inverted indexed table """
    if word in dict:
        return word
    else:
        return edit_dis(word)

## returns the word with minimum edit distance ##
def edit_dis(word):
    """Calculates the token with minimum edit distance"""
    min_dis = 100000
    min_token =""
    for token in dict:
        distance = nltk.edit_distance(token,word)
        if distance<min_dis:
            min_dis = distance
            min_token = token
    return min_token


########## Wildcard queries ##########

## gets all permutation for the given word ##
def rotate(str, n):
    """Gets all permutations for the given word"""
    return str[n:] + str[:n]

permuterm = {}

### adding entries in dict permuterm ###
keys = dict.keys()
for key in sorted(keys): ## gets words from inveted index 
    dkey = key + "$"
    for i in range(len(dkey),0,-1):
        out = rotate(dkey,i)  
        if out not in permuterm:
          permuterm[out] = [key]


## matches the prefix of given word from perterm dictionary ##
## returns list of matched terms ##
def prefix_match(term, prefix):
    """Matches the prefix of the given token with tokens in the permuterm dictionary"""
    term_list = []
    for tk in term.keys():
        if tk.startswith(prefix):
            term_list.append(term[tk])
    return term_list

## gets documents from matched words ##
def processQuery(query):  
    """Gets all documents which matched the word"""  
    term_list = prefix_match(permuterm,query)  ### got the words   
    filename = []
    for term in term_list:
        filename.append(dict[term[0]])

    temp = []
    for x in filename:
        for y in x:
          if (y not in temp):
            temp.append(y)
    print("DOCUMENTS RETRIEVED")
    print(temp)        
 
 # takes in the input query ##
query =""
while(1):
    
    query = input('Enter Query : ')
    start = time.time()
    if (query == "EXIT"):  ## runs until recieves "EXIT"
        break

    if query.find("*") != -1:  ## if it is a wildcard query
        parts = query.split("*")

        if parts[1] == '': # matchs with query of type X*
            case = 1
        elif parts[0] == '': # matchs with query of type *X
            case = 2
        elif parts[0] != '' and parts[1] != '': # matchs with query of type X*Y
            case = 3

        if case == 1:
            query = parts[0]
        elif case == 2:
            query = parts[1] + "$"
        elif case == 3:
            query = parts[1] + "$" + parts[0]

        processQuery(query)
    else: 
        bool_query(query)   # for boolean query
        print("DOCUMENTS RETRIEVED \n",operand[0])
        operand.clear()


    end = time.time()
    print("The execution time is :", end-start)

