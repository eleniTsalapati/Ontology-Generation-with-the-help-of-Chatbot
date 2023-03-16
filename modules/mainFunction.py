from cgitb import reset
from re import sub
import modules.chatbotTalks as talk
import modules.ontologyManager as manager
import modules.chatbotHears as hear
import modules.utility as utility


def Sentence(sentence,ui):
    # See what the ontology should answer
    (ui.nouns,ui.relationships)=hear.WhatOntologyToAnswer(sentence,ui)
    ui.taskNouns=len(ui.nouns.keys())
    ui.checkTask()

def narrow(data,parent,ui):
    # find the children
    inside,outside=hear.FindNounsInDataBase(parent,data,ui)
    # if they are in the database
    for noun in inside:
        addInheritance(noun,[parent],data,ui)
    # for each type from the different types 
    for noun in outside:            
        createNoun(noun,[parent],data,ui,False)

def broaden(data,ui):
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

def destroy(data,ui):
    ui.makeTables(data)
    # find the classes and the relationships
    classes,relationships_others=utility.FindNounsInDataBase(data,ui,"Which Class or relationship should I destroy?")
    utility.deleteData(data,ui,classes,relationships_others,True)
    