import chatbotTalks as talk
import ontologyCreation as creation
import chatbotHears as hear


# Load the ontology
ontology=creation.LoadOntology("file:////media/akis/Ubuntu-Windows/Uni/Chatbot-for-Ontology-Generation/ontologies/ChatBot.owl")

talk.FirstQuestion()
(nouns,relationships)=hear.WhatOntologyToAnswer()
print(nouns)
print(relationships)

# For all the nouns that we have
for noun in nouns.keys():
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
            definition="I FOUND THE DEFINITION" 
            definedBy="Search Engine"

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
            # The user doesnt want to keep the word
            else:
                continue
    
    # Create into the ontology the word
    theClass=creation.CreateObject(ontology,noun,nouns[noun])
    # and give the definition
    if definition!="":
        creation.Explaination(ontology,theClass,definition,definedBy)

# Save the ontology
creation.SaveOntology(ontology)
