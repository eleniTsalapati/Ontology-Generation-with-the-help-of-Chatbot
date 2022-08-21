#  -----------------------------------------------------------------------------------------------------------------
#                                        main talks
#  -----------------------------------------------------------------------------------------------------------------


def Welcome():
    txt="Welcome, User!\n"
    txt+="This Chatbot is made to create an Ontology.\n"
    txt+="I will ask you questions about the ontology and you have to answer them.\n"
    txt+="Let's start!!\n\n"
    txt+="In which file shall I save the ontology?\n"
    txt+="IMPORTANT: If the file path is local then it has to begin with file://\n"
    txt+="           If the file path is digital then it has to begin with http://\n"
    print(txt)
    return txt
    
def WhatOntologyToAnswer():
    txt="What questions do you want your ontology to be able to answer?\n"
    print(txt)
    return txt

def CouldNotUnderstand(txt):
    txt2="Sorry but I could not understand your answer.\n\n"
    print(txt2)
    return txt2+txt

def FindDefinition(word):
    txt="Shall I search for the definition of  \""+ word +"\"?\n"
    print(txt)
    return txt

def AskDefinition(word):
    txt="Do you want to give your own definition for  \""+ word +"\"?\n"
    print(txt)
    return txt

def YourDefinition(word):
    txt="What is your definition of  \""+ word +"\"?\n"
    print(txt)
    return txt

def KeepWord(word):
    txt="Shall I keep  \"" + word + "\" without a definition?\n"
    txt+="If the answer is negative then the ontology will not keep this word.\n"
    print(txt)
    return txt

def AskDifferentTypes(word):
    txt="Are there different types of  \""+ word +"\"?\n"
    print(txt)
    return txt

def GetDifferentTypes(word):
    txt="Enumerate all different types of  \""+ word +"\".\n"
    print(txt)
    return txt

def MoreOntology():
    txt="Do you want the ontology to be able to answer more questions?\n"
    print(txt)
    return txt
    
def EnumerateTheClasses():
    txt="Do you want to enumerate the different types of words in the ontology?\n"
    txt+="IMPORTANT: If the answer is negative then the program will finish here and the ontology will be saved!\n"
    print(txt)
    return txt

def EndingStatement():
    txt="I would like to thank you for using this ChatBot to develop your ontology!\n"
    print(txt)
    return txt

#  -----------------------------------------------------------------------------------------------------------------
#                                        search Ontology talks
#  -----------------------------------------------------------------------------------------------------------------

def termFoundNoDescription(term,ontology):
    txt="The Ontology \""+ontology+"\" has no description for \""+term+"\".\n"
    txt+="Should I keep this ontology without a description?\n"
    txt+="If the answer is negative then this Ontology will be discarded and another Ontology will be searched.\n"
    print(txt)
    return txt

def termKeepKids(term):
    txt="Shall I keep the Kids of \""+term+"\"?\n"
    print(txt)
    return txt

def termKeepTheKidWithDescription(term,kid,description,ontology):
    txt="The Ontology \""+ontology+"\" has \""+kid+"\" as kid of \""+term+"\" with the description:\n"
    txt+=description+"\n"
    txt+="Shall I keep this kid?\n"
    print(txt)
    return txt

def termNoKidFound(term,ontology):
    txt="The ontology \""+ontology+"\" has no kids for \""+term+"\".\n\n"
    print(txt)
    return txt

def termKeepTheKidWithoutDescription(term,kid,ontology):
    txt="The Ontology \""+ontology+"\" has \""+kid+"\" as kid of \""+term+"\" without a description.\n"
    txt+="Shall I keep this kid?\n"
    print(txt)
    return txt

def termFoundDescription(term,description,ontology):
    txt="The Ontology \""+ontology+"\" has the following description for \""+term+"\":\n"
    txt+=description+"\n"
    txt+="Shall I keep this ontology with a description\n"
    txt+="If the answer is negative then this Ontology will be discarded and another Ontology will be searched.\n"
    print(txt)
    return txt


