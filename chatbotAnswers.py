import nltk
# TO DO: See the list that you have to download to work as nltk
# What questions do you want your ontology to be able to answer

# A:Enumerate all remote sensors from satellites 
def WhatOntologyToAnswer():
    objects={}
    answer=input()
    tokens=nltk.word_tokenize(answer.lower())
    tagged=nltk.pos_tag(tokens)

    flag=False
    previous=None
    theWord=""

    for word in tagged:
        if 'JJ' == word[1]:
            theWord = theWord+" "+ word[0]

        if 'NNS' == word[1] or 'NN' == word[1]:
            theWord = theWord+" "+ word[0]
            if flag==False:
                objects[theWord]=None
            else:
                objects[theWord]=previous
            theWord=""

        if 'POS' in word[1]:
            print("yes")
            flag=True
        else :
            flag=False
            previous=theWord

    print(objects)
    return tagged