import modules.chatbotTalks as talk
import modules.ontologyCreation as creation
import modules.chatbotHears as hear
import modules.searchOntology as search
import modules.utility as utility

def find_definition_of_Noun(noun):
    kids=None
    definition=None
    
    answer= utility.question_Noun_with_yes_or_No(talk.FindDefinition,noun)
        
    # The user wants to find the definition
    if answer==1:
        # search the definition
        (definition,definedBy,kids)=search.searchForTerm(noun)
        
    # if the search definition was not selected
    if  definition==None:

        # ask if the user want to give definition
        answer= utility.question_Noun_with_yes_or_No(talk.AskDefinition,noun)

        # The user wants to give the definition
        if answer == 1:
            talk.YourDefinition(noun)
            definition=hear.GetDefinition()
            definedBy="You"
        # The user wants to do something else
        else:
            # See if the user wants to keep without definition
            answer= utility.question_Noun_with_yes_or_No(talk.KeepWord,noun)
            
            # The user wants to keep without definition
            if answer==1:
                definition=""
                definedBy=""
            # The user does not want to keep the word
            else:
                definition=None
                definedBy=None

    return (definition,definedBy,kids)

def what_the_ontology_should_answer(ontology,classes):

    previousNouns=classes[0].keys()
    previousRelated=classes[1].keys()

    # See what the ontology should answer
    talk.WhatOntologyToAnswer()
    (nouns,relationships)=hear.WhatOntologyToAnswer()

    # For all the nouns that we have
    for noun in nouns.keys():

        # we have already seen this noun in a previous question
        if noun in previousNouns:
            continue
        
        # find the definition of the noun
        (definition,definedBy,kids)=find_definition_of_Noun(noun)

        # if the user do not want to keep the noun 
        if  definition==None:
            continue
        
        # Create into the ontology the word
        classes[0][noun]=creation.CreateObject(ontology,noun,nouns[noun])
        # and give the definition
        if definition!="":
            creation.Explanation(ontology,classes[0][noun],definition,definedBy)

        # check if there were any kids
        if kids !=None:
            # for all the kids
            for (kid,definition,definedBy) in kids:
                # Create the kid 
                classes[0][kid]=creation.CreateObject(ontology,kid,classes[0][noun])
                # add the definition
                if definition!="":
                    creation.Explanation(ontology,classes[0][kid],definition,definedBy)

    # for all relationships
    keptNouns=classes[0].keys()
    for relation in relationships.keys():
        # we have already seen this relation in a previous question
        if relation in previousRelated:
            continue

        # if one object is not created then do not create the relationship
        obj1=relationships[relation][0]
        obj2=relationships[relation][1]
        if obj1 not in keptNouns or obj2 not in keptNouns:
            continue

        # create the relationship
        classes[1][relation]=creation.ConnectObjects(ontology,relation,classes[0][obj1],classes[0][obj2])

def more_types(ontology,classes,seen):
    
    nouns=list(classes[0].keys())
    for noun in nouns:

        # if the noun has already been seen 
        # do not ask for more types
        if noun in seen:
            continue

        seen.append(noun)
        
        # ask if you want to get the different types
        answer= utility.question_Noun_with_yes_or_No(talk.AskDifferentTypes,noun)
        if answer==1:

            # ask the types
            talk.GetDifferentTypes(noun)
            types=hear.GetTypes()

            # for each type from the different types 
            for type in types:
            
                (definition,definedBy,kids)=find_definition_of_Noun(type)
            
                if  definition==None:
                    continue

                # Create into the ontology the word
                classes[0][type]=creation.CreateObject(ontology,type,classes[0][noun])
                # and give the definition
                if definition!="":
                    creation.Explanation(ontology,classes[0][type],definition,definedBy)

                if kids !=None:
                    for (kid,definition,definedBy) in kids:
                        classes[0][kid]=creation.CreateObject(ontology,kid,classes[0][noun])
                        if definition!="":
                            creation.Explanation(ontology,classes[0][kid],definition,definedBy)

                
# -------------------------------------------------------
#                       main
# -------------------------------------------------------

# classes=[classesObj,classesRel]
classes=[{},{}]
seen=[]
# Welcome
talk.Welcome()

# Load the ontology
answer = None
while answer == None:
    talk.askTheFile()
    answer=hear.thePath()
    if answer==None:
        talk.CouldNotUnderstand()

ontology=creation.LoadOntology(answer)


what_the_ontology_should_answer(ontology,classes)

while(True):
    answer= utility.question_with_yes_or_No(talk.MoreOntology)

    if answer == 1:
        what_the_ontology_should_answer(ontology,classes)
        continue

    answer= utility.question_with_yes_or_No(talk.EnumerateTheClasses)

    if answer == 1:
        more_types(ontology,classes,seen)
        continue
    break

# Save the ontology
creation.SaveOntology(ontology)
talk.EndingStatement()
