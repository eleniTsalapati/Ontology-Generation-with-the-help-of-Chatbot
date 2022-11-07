from cgitb import reset
from re import sub
import modules.chatbotTalks as talk
import modules.ontologyManager as manager
import modules.chatbotHears as hear
import modules.utility as utility
from modules.creationFunctions import *

def Sentence(data,ui):

    # See what the ontology should answer
    ui.makeTables(data)
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
        createRelation(data,ui,obj1,relation,obj2)

def specialize(data,ui):
    ui.makeTables(data)
    parents,_=utility.FindNounsInDataBase(data,ui,talk.WhatToSpecialize())
    for parent in parents:        
        ui.makeTables(data)
        inside,outside=utility.FindNounsInDataBase(data,ui,talk.WhatIsTheSpecialization(parent))
        # if they are in the database
        for noun in inside:
            addInheritance(noun,[parent],data,ui)
        # for each type from the different types 
        for noun in outside:            
            createNoun(noun,[parent],data,ui,False)

def generalized(data,ui):
    ui.makeTables(data)
    inside,outside=utility.FindNounsInDataBase(data,ui,talk.WhatIsTheGeneralization())
    for parent in outside:
        if createNoun(parent,[],data,ui,False)==False:
            ui.changeMessage("Something went wrong with saving the word\n")

    for parent in inside+outside:        
        if parent not in data[0].keys():
            continue

        ui.makeTables(data)
        nouns,_=utility.FindNounsInDataBase(data,ui,talk.WhatToGeneralize(parent))
        if nouns==[]:
            ui.rememberOneTime("No data was found\n")
            continue
        
        for noun in nouns:
            addInheritance(noun,[parent],data,ui)
