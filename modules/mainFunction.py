from cgitb import reset
from re import sub
import modules.chatbotTalks as talk
import modules.ontologyManager as manager
import modules.chatbotHears as hear
import modules.searchOntology as search
import modules.utility as utility
from modules.classCreation import *

def Sentence(data,ui):

    # See what the ontology should answer
    ui.changeMessage(talk.WhatOntologyToAnswer())
    answerUI=ui.hear()
    (nouns,relationships)=hear.WhatOntologyToAnswer(answerUI,ui)

    # For all the nouns that we have
    for noun in nouns.keys():
        parent=nouns[noun]

        # find the definition of the noun
        if parent==None:
            createNoun(noun,[],data,ui)
        else:
            createNoun(noun,[parent],data,ui)


    # for all relationships
    for relation in relationships.keys():

        # if one object is not created then do not create the relationship
        obj1=relationships[relation][0]
        obj2=relationships[relation][1]

        # one object was not kept
        if obj1 not in data[0].keys() or obj2 not in data[0].keys():
            continue

        relation=relation+obj2.title()

        # mark as used
        data[0][obj1][3]=1
        data[0][obj2][3]=1

        if relation not in data[1].keys():
            # create the relationship
            data[1][relation]=[manager.ConnectObjects(data[2],relation,data[0][obj1][0],data[0][obj2][0]),[obj1],relation,obj2]
        else:
            manager.AddConnection(data[2],data[1][relation][0],data[0][obj1][0])
            data[1][relation][1].append(obj1)


def specialize(data,ui):
    ui.changeMessage("Which words from the dataBase do you want to specialize?\nGive it as it is in the DataBase\n")
    answerUI=ui.hear()
    nouns=hear.FindNounsInDataBase(answerUI,data,ui)
    for noun in nouns:        
        ui.rememberTableOnce()
        ui.changeMessage(talk.GetDifferentTypes(noun))
        answerUI=ui.hear()
        types=hear.GetNouns(answerUI,ui)

        # for each type from the different types 
        for type in types:            
            createNoun(type,[noun],data,ui,False)

def generalized(data,ui):
    ui.changeMessage("Which words do you want to add?")
    answerUI=ui.hear()
    nouns=hear.GetNouns(answerUI,ui)
    for noun in nouns:        
        ui.rememberTableOnce()
        ui.changeMessage("Which words from DataBase do you want to be categorized as generalized with the word\""+noun+"\"\n Give it as it is in the DataBase\n")
        answerUI=ui.hear()
        parents=hear.FindNounsInDataBase(answerUI,data,ui)
        if parents==None:
            ui.rememberOneTime("No data was found\n")
        else:
            createNoun(noun,parents,data,ui,False)
