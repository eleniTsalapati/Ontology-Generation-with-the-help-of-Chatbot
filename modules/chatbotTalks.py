#  -----------------------------------------------------------------------------------------------------------------
#                                        main talks
#  -----------------------------------------------------------------------------------------------------------------


def Welcome():
    print("Welcome, User!")
    print("This Chatbot is made to create an Ontology.")
    print("I will ask you questions about the ontology and you have to answer them.")
    print("Let's start!!")
    print()

def askTheFile():
    print("In which file shall I save the ontology?")
    print("IMPORTANT: If the file path is local then it has to begin with file://")
    print("           If the file path is digital then it has to begin with http://")

def GetOntology():
    print("From which file do you want the ontology to be saved?")
    
def WhatOntologyToAnswer():
    print("What questions do you want your ontology to be able to answer?")

def CouldNotUnderstand():
    print("Sorry but I could not understand your answer.")

def AskDefinition(word):
    print("Do you want to give your own definition for  \""+ word +"\"?")

def YourDefinition(word):
    print("What is your definition of  \""+ word +"\"?")

def FindDefinition(word):
    print("Shall I search for the definition of  \""+ word +"\"?")

def KeepWord(word):
    print("Shall I keep  \"" + word + "\" without a definition?")
    print("If the answer is negative then the ontology will not keep this word.")

def AskDifferentTypes(word):
    print("Are there different types of  \""+ word +"\"?")

def GetDifferentTypes(word):
    print("Enumerate all different types of  \""+ word +"\".")

def MoreOntology():
    print("Do you want the ontology to be able to answer more questions?")
    
def EnumerateTheClasses():
    print("Do you want to enumerate the different types of words in the ontology?")
    print("IMPORTANT: If the answer is negative then the program will finish here and the ontology will be saved!")

def EndingStatement():
    print("I would like to thank you for using this ChatBot to develop your ontology!")

#  -----------------------------------------------------------------------------------------------------------------
#                                        search Ontology talks
#  -----------------------------------------------------------------------------------------------------------------

def termFoundNoDescription(term,ontology):
    print("The Ontology \""+ontology+"\" has no description for \""+term+"\".")
    print("Should I keep this ontology without a description?")
    print("If the answer is negative then this Ontology will be discarded and another Ontology will be searched.")

def termKeepKids(term):
    print("Shall I keep the Kids of \""+term+"\"?")

def termKeepTheKidWithDescription(term,kid,description,ontology):
    print("The Ontology \""+ontology+"\" has \""+kid+"\" as kid of \""+term+"\" with the description:")
    print(description)
    print("Shall I keep this kid?")

def termNoKidFound(term,ontology):
    print("The ontology \""+ontology+"\" has zero(0) kids for \""+term+"\".")

def termKeepTheKidWithoutDescription(term,kid,ontology):
    print("The Ontology \""+ontology+"\" has \""+kid+"\" as kid of \""+term+"\" without a description.")
    print("Shall I keep this kid?")

def termFoundDescription(term,description,ontology):
    print("The Ontology \""+ontology+"\" has the following description for \""+term+"\":")
    print(description)
    print("Shall I keep this ontology with a description?")
    print("If the answer is negative then this Ontology will be discarded and another Ontology will be searched.")

