import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()
    
# TO DO: See the list that you have to download to work as nltk
# What questions do you want your ontology to be able to answer

# A:Enumerate all remote sensors from satellites 
def WhatOntologyToAnswer():
    nouns={}
    relationships={}
    flagRelationships=False
    answer=input()
    print(answer)
    tokens=nltk.word_tokenize(answer.lower())
    tagged=nltk.pos_tag(tokens)

    flag=False
    previous=None
    theWord=""
    verb=""

    for word in tagged:
        
        if 'JJ' == word[1] or 'JJR' == word[1] or 'JJS' == word[1]:
            if theWord!="":
                theWord = theWord+" "+ word[0]
            else:
                theWord = word[0]
        
        elif 'NNS' == word[1] or 'NN' == word[1] or 'NNS' == word[1] or 'NNP' == word[1] or 'NNPS' == word[1]:
            if theWord!="":
                theWord = theWord+" "+ word[0]
            else:
                theWord = word[0]

            if flagPOS==False:
                nouns[theWord]=None
            else:
                nouns[theWord]=previous
            if flagRelationships==True:
                relationships[theRelation].append(theWord)
                flagRelationships=False
            previous=theWord
            theWord=""

        elif 'IN' == word[1] or 'TO'==word[1]:
            if verb!="":
                verb = verb+" "+ word[0]
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
                verb = verb+" "+ word[0]
            else:
                verb = word[0]
        else:
            verb=""        
            
        if 'POS' in word[1]:
            flagPOS=True

        else :
            flagPOS=False

    return (nouns,relationships)

def GetTrueOrFalse():
    answer=input()
    print(answer)
    polarity=sia.polarity_scores(answer.lower())
    if polarity['neg']<polarity['pos']:
        return 1
    elif polarity['neg']>polarity['pos']:
        return -1
    else:
        return 0

def GetDefinition():
    answer=input()
    print(answer)
    return answer