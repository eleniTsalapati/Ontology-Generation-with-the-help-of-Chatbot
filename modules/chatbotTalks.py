#  -----------------------------------------------------------------------------------------------------------------
#                                        main talks
#  -----------------------------------------------------------------------------------------------------------------

def Welcome():
    txt="Welcome, User!\n"
    txt+="This Chatbot is made to create an Ontology.\n"
    txt+="I will ask you questions about the ontology and you have to answer them.\n"
    txt+="Let's start!!\n\n"
    txt+="In which file shall I save the ontology?\n"
    txt+="IMPORTANT!!\n"
    txt+="If the file path is local then it has to begin with \"file://\" "
    txt+="or you can search the local file from the button \"Find File\"\n"
    txt+="If the file path is digital then it has to begin with \"http://\"\n"
    print(txt)
    return txt
    
def WhatOntologyToAnswer():
    txt="What questions do you want your ontology to be able to answer?\n\n"
    txt+="Please be careful with the grammar, syntax of the answer as it will affect it."
    print(txt)
    return txt

def CouldNotUnderstand():
    txt="\n\n Sorry but I could not understand your answer.\n\n"
    print(txt)
    return txt

def AskDifferentTypes(word):
    txt="Are there different subcategories of  \""+ word +"\"?\n"
    print(txt)
    return txt

def GetDifferentTypes(word):
    txt="Enumerate all different subcategories of  \""+ word +"\".\n"
    print(txt)
    return txt

def MoreOntology():
    txt="Do you want the ontology to be able to answer more questions?\n"
    print(txt)
    return txt
    
def EnumerateTheClasses():
    txt="Do you want to enumerate the different subcategories of words in the ontology?\n"
    print(txt)
    return txt

def AddHyperClass():
    txt="Do you want to add a hyper class into your ontology?\n"
    txt+="Meaning that the subjects that you have to be made subcategories\n\n"
    txt+="IMPORTANT: If the answer is negative then the program will finish here and the ontology will be saved!\n"
    print(txt)
    return txt

def AskForHyper():
    txt="What new word do you want to become Hyper?\n"
    print(txt)
    return txt

def DefineHyper(word):
    txt="Can you give the name of the HyperClass of \""+word+"\" ?\n"
    print(txt)
    return txt

def AskHyperOfHyper(word):
    txt="Do you want to add a HyperClass for \""+word+"\"?\n"
    print(txt)
    return txt

def FindHyperOfHyper(word):
    txt="What is the HyperClass of \""+word+"\"?\n"
    print(txt)
    return txt

def BecomeHyper(word):
    txt="Which words from those you used, do you want to be subcategory of \""+word+"\"?\n"
    print(txt)
    return txt

#  -----------------------------------------------------------------------------------------------------------------
#                                        Definition
#  -----------------------------------------------------------------------------------------------------------------

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

#  -----------------------------------------------------------------------------------------------------------------
#                                        search Ontology talks
#  -----------------------------------------------------------------------------------------------------------------

def termFoundNoDescription(term,ontology):
    txt="The Ontology \""+ontology+"\" has no description for \""+term+"\".\n"
    txt+="Should I keep this ontology without a description?\n"
    txt+="If the answer is negative then this Ontology will be discarded and another Ontology will be searched.\n"
    print(txt)
    return txt

def termKeepSubcategories(term):
    txt="Shall I keep the subcategories of \""+term+"\"?\n"
    print(txt)
    return txt

def termKeepTheSubcategoryWithDescription(term,subcategory,description,ontology):
    txt="The Ontology \""+ontology+"\" has \""+subcategory+"\" as subcategories of \""+term+"\" with the description:\n"
    txt+=description+"\n"
    txt+="Shall I keep this subcategories?\n"
    print(txt)
    return txt

def termNoSubcategoryFound(term,ontology):
    txt="The ontology \""+ontology+"\" has no subcategories for \""+term+"\".\n\n"
    print(txt)
    return txt

def termKeepTheSubcategoryWithoutDescription(term,subcategory,ontology):
    txt="The Ontology \""+ontology+"\" has \""+subcategory+"\" as subcategories of \""+term+"\" without a description.\n"
    txt+="Shall I keep this subcategories?\n"
    print(txt)
    return txt

def termFoundDescription(term,description,ontology):
    txt="The Ontology \""+ontology+"\" has the following description for \""+term+"\":\n"
    txt+=description+"\n"
    txt+="Shall I keep this ontology with a description\n"
    txt+="If the answer is negative then this Ontology will be discarded and another Ontology will be searched.\n"
    print(txt)
    return txt

def seen5Sub(term):
    txt="You have seen 5 subcategories of \""+term+"\"\n Do you want to see more?\n"
    return txt
#  -----------------------------------------------------------------------------------------------------------------
#                                        Onto Clean
#  -----------------------------------------------------------------------------------------------------------------

def ontoCheck(parent,child):
    txt="Is \""+child+"\" a kind of \"" + parent +"\"?\n"
    txt+="For example: Is every \"" + child + "\" also \""+parent+"\".\n"
    return txt

def identityComponentOf(first,second):
    txt="Is the \""+first+"\" component of \"" + second +"\"?\n"
    txt+="For example: Is every \"" + first + "\" component of \""+second+"\".\n"
    return txt

def unityComposedOf(first,second):
    txt="Is the \""+first+"\" composed of \"" + second +"\"?\n"
    txt+="For example: Is every \"" + first + "\" composed of \""+second+"\".\n"
    return txt
