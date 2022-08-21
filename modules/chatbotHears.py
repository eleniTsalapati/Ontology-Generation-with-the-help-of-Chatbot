from nltk import word_tokenize,pos_tag
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer

sia = SentimentIntensityAnalyzer()
lemmatizer = WordNetLemmatizer()

def WhatOntologyToAnswer(answer):
    print(answer)
    print()

    # tokenize and take tags of the words
    tokens=word_tokenize(answer.lower())
    tagged=pos_tag(tokens)

    # define
    nouns={}
    relationships={}
    flagRelationships=False
    flagPOS=False
    previous=None
    flagPrint= False
    theWord=""
    verb=""

    for word in tagged:

        # if the word is adj just add it to the word 
        if 'JJ' == word[1] or 'JJR' == word[1] or 'JJS' == word[1]:
            if theWord!="":
                theWord = theWord+ " " +word[0]
            else:
                theWord = word[0]
        
        # if the the word is noun
        elif 'NN' == word[1] or 'NNS' == word[1] or 'NNP' == word[1] or 'NNPS' == word[1]:

            # Singularize or lemmatize the word to be singular
            if 'NNS' == word[1] or 'NNPS' == word[1]:
                if lemmatizer.lemmatize(word[0])!= []:
                    print("Lemmatize the \""+word[0]+"\" to \""+lemmatizer.lemmatize(word[0])+"\"")
                    word=(lemmatizer.lemmatize(word[0]),word[1])
                    flagPrint=True
                else:
                    print("I cannot lemmatize the \""+word[0]+"\"") 

            # add it to the word
            if theWord!="":
                theWord = theWord+ " " +word[0]
            else:
                theWord = word[0]

            # add the word with possessive argument if need be
            if flagPOS==False:
                nouns[theWord]=None
            else:
                nouns[theWord]=previous

            # if a relation needs this word add it
            if flagRelationships==True:
                relationships[theRelation].append(theWord)
                flagRelationships=False

            # re-initialize
            previous=theWord
            theWord=""

        # create a relation
        elif 'IN' == word[1] or 'TO'==word[1]:
            # check if there is a verb for TO
            if verb!="":
                verb = verb+ " "+word[0]
            else:
                verb = word[0]

            relationships[verb]=[previous]
            theRelation=verb
            verb=""
            flagRelationships=True

        if 'VB' == word[1] or 'VBG' == word[1] or\
             'VBP' == word[1] or 'VBD' == word[1] or\
             'VBZ' == word[1] or 'VBN' == word[1] :
            if verb!="":
                verb = verb+ " "+word[0]
            else:
                verb = word[0]
        else:
            verb=""        
            
        if 'POS' in word[1]:
            flagPOS=True

        else :
            flagPOS=False

    if flagPrint:
        print()

    return (nouns,relationships)

def GetTrueOrFalse(answer):
    print(answer)
    print()
    
    polarity=sia.polarity_scores(answer.lower())
    if polarity['neg']<polarity['pos']:
        return 1
    elif polarity['neg']>polarity['pos']:
        return -1
    else:
        return 0

def GetDefinition(answer):
    print(answer)
    print()
    
    return answer

def thePath(answer):
    print(answer)
    print()
    
    tokens=answer.split()
    for token in tokens:
        if "file://" in token:
            return token
        elif "http://" in token:
            return token
    return None

def GetTypes(answer):
    print(answer)
    print()

    # tokenize and take tags of the words
    tokens=word_tokenize(answer.lower())
    tagged=pos_tag(tokens)

    # define
    nouns=[]
    theWord=""

    for word in tagged:

        # if the word is adj just add it to the word 
        if 'JJ' == word[1] or 'JJR' == word[1] or 'JJS' == word[1]:
            if theWord!="":
                theWord = theWord+ " "+word[0]
            else:
                theWord = word[0]
        
        # if the the word is noun
        elif 'NNS' == word[1] or 'NN' == word[1] or 'NNS' == word[1] or 'NNP' == word[1] or 'NNPS' == word[1]:
            
            # Singularize or lemmatize the word to be singular
            if 'NNS' == word[1] or 'NNPS' == word[1]:
                if lemmatizer.lemmatize(word[0])!= []:
                    print("Lemmatize the \""+word[0]+"\" to \""+lemmatizer.lemmatize(word[0])+"\"")
                    word=(lemmatizer.lemmatize(word[0]),word[1])
                    flagPrint=True
                else:
                    print("I cannot lemmatize the \""+word[0]+"\"") 

            # add it to the word
            if theWord!="":
                theWord = theWord+" "+word[0]
            else:
                theWord = word[0]

            nouns.append(theWord)
            theWord=""

    return nouns
