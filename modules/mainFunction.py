from cgitb import reset
from re import sub
import modules.chatbotTalks as talk
import modules.ontologyManager as manager
import modules.chatbotHears as hear
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

        relation=obj1.title()+"_"+relation.title()+"_"+obj2.title()

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
    ui.changeMessage("Which words from the dataBase do you want to specialize? In essence, you will add a(n) (inheritance)child to this word.\nGive it as it is in the DataBase\n\n For example if we have animal-horse(-mule) and we want to add mule to horse then give the horse.\n")
    answerUI=ui.hear()
    parents,_=hear.FindNounsInDataBase(answerUI,data,ui)
    for parent in parents:        
        ui.makeTables(data)
        ui.changeMessage("Which words do you want to give as specialization (inheritance child) of "+parent+"(inheritance parent)?\n The words can be inside the DataBase (give it as it is) or outside of it.\n\n For example, if we have animal-horse(-mule) and we want to add mule to horse then give the mule.\n")
        answerUI=ui.hear()
        inside,outside=hear.FindNounsInDataBase(answerUI,data,ui)
        # if they are in the database
        for noun in inside:
            addInheritance(noun,[parent],data,ui)

        # for each type from the different types 
        for noun in outside:            
            createNoun(noun,[parent],data,ui,False)

def generalized(data,ui):
    ui.makeTables(data)
    ui.changeMessage("Which words do you want to give as generalization(inheritance parent)?\n\nFor example, if we have (animal-)horse-mule and we want to add animal to horse then give the animal\n It can be in the DataBase or not.\n")
    answerUI=ui.hear()
    inside,outside=hear.FindNounsInDataBase(answerUI,data,ui)
    for parent in outside:
        if createNoun(parent,[],data,ui,False)==False:
            ui.changeMessage("Something went wrong with saving the word\n")

    for parent in inside+outside:        
        if parent not in data[0].keys():
            continue

        ui.makeTables(data)
        ui.changeMessage("Which words do you want to give to be generalized(inheritance child) from \""+parent+"\" (inheritance parent)?\nIn essence, with which words the generalized word "+parent+" you gave is linked to?\n\nFor example if we have (animal-)horse-mule and we want to add animal to horse then give the horse\n")
        answerUI=ui.hear()
        nouns,_=hear.FindNounsInDataBase(answerUI,data,ui)
            
        if nouns==[]:
            ui.rememberOneTime("No data was found\n")
            continue
        for noun in nouns:
            addInheritance(noun,[parent],data,ui)
