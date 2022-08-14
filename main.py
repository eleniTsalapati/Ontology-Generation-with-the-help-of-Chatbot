import modules.chatbotTalks as talk
import modules.ontologyCreation as creation
import modules.chatbotHears as hear
import modules.searchOntology as search

def getNoun(noun):
    kids=None
    # See if the user wants to give the definition
    answer=0
    while answer==0 :
        talk.AskDeffinition(noun)
        answer=hear.GetTrueOrFalse()
        if answer==0:
            talk.CouldNotUnderstand()

    # The user wants to give the definition
    if answer == 1:
        talk.YourDefinition(noun)
        definition=hear.GetDefinition()
        definedBy="You"
    # The user wants to do something else
    else:
        # See if the user wants to find an existing definition
        answer=0
        while answer==0 :
            talk.FindDefinition(noun)
            answer=hear.GetTrueOrFalse()
            if answer==0:
                talk.CouldNotUnderstand()
        
        # The user wants to find the definition
        if answer==1:
            (definition,definedBy,kids)=search.searchForTerm(noun)
            if definition==None:

                answer=0
                while answer==0 :
                    talk.AskDeffinition(noun)
                    answer=hear.GetTrueOrFalse()
                    if answer==0:
                        talk.CouldNotUnderstand()

                # The user wants to give the definition
                if answer == 1:
                    talk.YourDefinition(noun)
                    definition=hear.GetDefinition()
                    definedBy="You"
                # The user wants to do something else
                else:
                    # See if the user wants to keep without definition
                    answer=0
                    while answer==0 :
                        talk.KeepWord(noun)
                        answer=hear.GetTrueOrFalse()
                        if answer==0:
                            talk.CouldNotUnderstand()
                    
                    # The user wants to keep without definition
                    if answer==1:
                        definition=""
                        definedBy=""
                    # The user doesnt want to keep the word
                    else:
                        definition=None
                        definedBy=None
            

        # The user wants to do something else
        else:

            # See if the user wants to keep without definition
            answer=0
            while answer==0 :
                talk.KeepWord(noun)
                answer=hear.GetTrueOrFalse()
                if answer==0:
                    talk.CouldNotUnderstand()
            
            # The user wants to keep without definition
            if answer==1:
                definition=""
                definedBy=""
            # The user doesnt want to keep the word
            else:
                definition=None
                definedBy=None
    return (definition,definedBy,kids)

def AnswerOntology(ontology,classes):

    previousNouns=classes[0].keys()
    previousRelat=classes[1].keys()

    # See what the ontology should answer
    talk.WhatOntologyToAnswer()
    (nouns,relationships)=hear.WhatOntologyToAnswer()

    # For all the nouns that we have
    for noun in nouns.keys():

        # we have already seen this noun in a previous question
        if noun in previousNouns:
            continue
        
        (definition,definedBy,kids)=getNoun(noun)

        if  definition==None:
            continue
        
        # Create into the ontology the word
        classes[0][noun]=creation.CreateObject(ontology,noun,nouns[noun])
        # and give the definition
        if definition!="":
            creation.Explaination(ontology,classes[0][noun],definition,definedBy)

        if kids !=None:
            for (kid,definition,definedBy) in kids:
                classes[0][kid]=creation.CreateObject(ontology,kid,classes[0][noun])
                if definition!="":
                    creation.Explaination(ontology,classes[0][kid],definition,definedBy)

    # for all realationships
    keptNouns=classes[0].keys()
    for relation in relationships.keys():
        # we have already seen this relation in a previous question
        if relation in previousRelat:
            continue

        # if one object is not created then do not create the realationship
        obj1=relationships[relation][0]
        obj2=relationships[relation][1]
        if obj1 not in keptNouns or obj2 not in keptNouns:
            continue

        # create the realationship
        classes[1][relation]=creation.ConnectObjects(ontology,relation,classes[0][obj1],classes[0][obj2])

def MoreTypes(ontology,classes,seen):
    flag=False
    if len(seen)!=0:
        flag=True

    nouns=list(classes[0].keys())
    for noun in nouns:
        if flag==True:
            if noun in seen:
                continue

        seen.append(noun)
        answer=0
        while answer==0 :
            talk.AskDiffrentTypes(noun)
            answer=hear.GetTrueOrFalse()
            if answer==0:
                talk.CouldNotUnderstand()
        if answer==1:
            talk.GetDiffrentTypes(noun)
            types=hear.GetTypes()
            for type in types:
                (definition,definedBy,kids)=getNoun(type)
                if  definition==None:
                    continue

                # Create into the ontology the word
                classes[0][type]=creation.CreateObject(ontology,type,classes[0][noun])
                # and give the definition
                if definition!="":
                    creation.Explaination(ontology,classes[0][type],definition,definedBy)

                if kids !=None:
                    for (kid,definition,definedBy) in kids:
                        classes[0][kid]=creation.CreateObject(ontology,kid,classes[0][noun])
                        if definition!="":
                            creation.Explaination(ontology,classes[0][kid],definition,definedBy)

                
# -------------------------------------------------------
#                       main
# -------------------------------------------------------

# classes=[classesObj,classesRel]
classes=[{},{}]
seen=[]
# Welcome
talk.Welcome()

# Load the ontology
talk.askTheFile()
file=hear.thePath()
ontology=creation.LoadOntology(file)

AnswerOntology(ontology,classes)

while(True):
    answer=0
    while answer==0 :
        talk.MoreOntology()
        answer=hear.GetTrueOrFalse()
        if answer==0:
            talk.CouldNotUnderstand()
    if answer == 1:
        AnswerOntology(ontology,classes)
        continue

    answer=0
    while answer==0 :
        talk.EnumerateTheClasses()
        answer=hear.GetTrueOrFalse() 
        if answer==0:
            talk.CouldNotUnderstand()
    if answer == 1:
        MoreTypes(ontology,classes,seen)
        continue
    break

# Save the ontology
creation.SaveOntology(ontology)
talk.EndingStatement()
