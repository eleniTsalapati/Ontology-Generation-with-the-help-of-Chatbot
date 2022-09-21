from tkinter.tix import Tree
from nltk import word_tokenize,pos_tag
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer

sia = SentimentIntensityAnalyzer()
lemmatizer = WordNetLemmatizer()

def WhatOntologyToAnswer(answer,ui):
    print(">"+answer)
    print()

    # tokenize and take tags of the words
    tokens=word_tokenize(answer.lower())
    tagged=pos_tag(tokens)
    print(tagged)
    # define
    nouns={}
    relationships={}
    flagPOS=False
    previous=None
    theWord=""
    relation=""
    flagLem=False
    for word in tagged:

        # be sure that the VBN is correct tag due to some errors
        if 'VBN' == word[1]:
            word = pos_tag([word[0]])[0]

        # if the word is adj just add it to the word 
        if 'JJ' == word[1] or 'JJR' == word[1] or 'JJS' == word[1]:
            if theWord!="":
                theWord = theWord+word[0].title()
            else:
                theWord = word[0]
        
        # if the the word is noun
        elif 'NN' == word[1] or 'NNS' == word[1] or 'NNP' == word[1] or 'NNPS' == word[1]:

            # Singularize or lemmatize the word to be singular
            if 'NNS' == word[1] or 'NNPS' == word[1]:
                theLementation=lemmatizer.lemmatize(word[0])
                if theLementation!= []:
                    ui.rememberOneTime("Lemmatize the \""+word[0]+"\" to \""+theLementation+"\"\n")
                    word=(theLementation,word[1])
                    flagLem=True
            # add it to the word
            if theWord!="":
                theWord = theWord+word[0].title()
            else:
                theWord = word[0]

            # add the word with possessive argument if need be
            if flagPOS==False:
                nouns[theWord]=None
            else:
                nouns[theWord]=previous

            # if a relation needs this word add it
            if relation!="":
                if previous!=None:
                    theRelation=relation
                    relationships[theRelation]=[previous,theWord]

            # re-initialize
            previous=theWord
            theWord=""
            relation=""

        # create a relation
        elif 'IN' == word[1] or 'TO'==word[1]:
            # check if there is a verb for TO
            if relation!="":
                relation = relation+word[0].title()
            else:
                relation = word[0]

        elif 'VB' == word[1] or 'VBG' == word[1] or\
             'VBP' == word[1] or 'VBD' == word[1] or\
             'VBZ' == word[1] or 'VBN' == word[1] :
            if relation!="":
                relation = relation+word[0].title()
            else:
                relation = word[0]
            
        if 'POS' in word[1]:
            flagPOS=True
        else :
            flagPOS=False
    
    if flagLem==True:
        ui.rememberOneTime("\n")

    return (nouns,relationships)

def GetTrueOrFalse(answer):
    print(">"+answer)
    print()
    
    polarity=sia.polarity_scores(answer.lower())
    if polarity['neg']<polarity['pos']:
        return 1
    elif polarity['neg']>polarity['pos']:
        return -1
    else:
        return 0

def GetDefinition(answer):
    print(">"+answer)
    print()
    
    return answer

def thePath(answer):
    print(">"+answer)
    print()

    # check if the answer is found
    tokens=answer.split()
    for token in tokens:
        # we want either to begin with file:// or http://
        if "file://" == token[0:7]:
            return token
        elif "http://" == token[0:7]:
            return token
    return None

def GetTypes(answer,uo):
    print(">"+answer)
    print()

    # tokenize and take tags of the words
    tokens=word_tokenize(answer.lower())
    tagged=pos_tag(tokens)

    # define
    nouns=[]
    theWord=""
    flagLem=False
    
    for word in tagged:

        # if the word is adj just add it to the word 
        if 'JJ' == word[1] or 'JJR' == word[1] or 'JJS' == word[1]:
            if theWord!="":
                theWord = theWord+word[0].title()
            else:
                theWord = word[0]
        
        # if the the word is noun
        elif 'NNS' == word[1] or 'NN' == word[1] or 'NNS' == word[1] or 'NNP' == word[1] or 'NNPS' == word[1]:
            
            # Singularize or lemmatize the word to be singular
            if 'NNS' == word[1] or 'NNPS' == word[1]:
                theLementation=lemmatizer.lemmatize(word[0])
                if theLementation!= []:
                    ui.rememberOneTime("Lemmatize the \""+word[0]+"\" to \""+theLementation+"\"\n")
                    word=(theLementation,word[1])
                    flagLem=True

            # add it to the word
            if theWord!="":
                theWord = theWord+word[0].title()
            else:
                theWord = word[0]

            nouns.append(theWord)
            theWord=""

    if flagLem==True:
        ui.rememberOneTime("\n")

    return nouns
