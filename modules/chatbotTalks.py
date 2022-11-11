#  -----------------------------------------------------------------------------------------------------------------
#                                        main talks
#  -----------------------------------------------------------------------------------------------------------------

def Welcome():
    txt="Welcome, User!\n"
    txt+="This chatbot will help you develop your ontology!\n"
    txt+="From the given sentences (competency questions) it can create:\n"
    txt+="  -Hierarchy of classes\n"
    txt+="  -Object properties\n"
    txt+="  -Domain and range restrictions of object properties\n\n"
    txt+="From the generalization, you can generalize an existing class (ie: create new Super Classes).\n\n"
    txt+="From the specialization, you can specialize an existing class (ie: create new Sub Classes).\n\n"
    txt+="Whenever this is possible external ontologies by https://www.ebi.ac.uk/ols/index are reused.\n"
    txt+="Let's start!!\n\n"
    txt+="In which file shall I save the ontology?\n\n"
    txt+="IMPORTANT!!\n\n"
    txt+="If the file is local then your answer has to begin with \"file://\" following the path file "
    txt+="or you can find the local file by using the button \"Find File\"\n\n"
    txt+="If the file is digital then it has to begin with \"http://\" following with the URL\n"
    return txt
    
def WhatOntologyToAnswer():
    txt="Give a Competency Question to add in the ontology?\n\n"
    txt+="If you have a lot of nouns, then you need to have underscore \"_\" in between the nouns. \n"
    txt+="For example: Mitigation_Action and NOT Mitigation action\n\n"
    txt+="Please be careful with the grammar(the articles), syntax of the answer as it will affect it.\n"
    txt+="Recognize: A cat eats fishes, Cats eat the fish\n"
    txt+="Not Recognize: Cat eat fish\n"
    return txt

def WhatToSpecialize():
    txt="Which classes from the ontology do you want to specialize?\n"
    txt+="In essence, you will add a(n) (inheritance) child to this class.\n"
    txt+="For example if we have animal-horse(-mule) and we want to add mule to horse then give the horse.\n\n"
    txt+="Give it as it is in the ontology\n\n"
    txt+="You can also select the class form the table down bellow.\n"
    return txt

def WhatIsTheSpecialization(parent):
    txt="Which classes do you want to give as specialization (inheritance child) of "+parent+" (inheritance parent)?\n"
    txt+="For example, if we have animal-horse(-mule) and we want to add mule to horse then give the mule.\n\n"
    txt+="The classes can be either be from the ontology or not.\n\n"
    txt+="You can also select the class form the table down bellow.\n"
    return txt

def WhatIsTheGeneralization():
    txt="Which classes do you want to give as generalization(inheritance parent)?\n"
    txt+="For example, if we have (animal-)horse-mule and we want to add animal to horse then give the animal\n\n"
    txt+="The classes can be either be from the ontology or not.\n\n"
    txt+="You can also select the class form the table down bellow.\n"
    return txt
    
def WhatToGeneralize(parent):
    txt="Which classes do you want to give to be generalized(inheritance child) from \""+parent+"\" (inheritance parent)?\n"
    txt+="In essence, with which classes the generalized class "+parent+" you gave is linked to?\n"
    txt+="For example if we have (animal-)horse-mule and we want to add animal to horse then give the horse\n\n"
    txt+="The classes can be either be from the ontology or not.\n\n"
    txt+="You can also select the class form the table down bellow.\n"
    return txt

def CouldNotUnderstand():
    txt="\n\n Sorry but I could not understand your answer.\n\n"
    return txt

#  -----------------------------------------------------------------------------------------------------------------
#                                        Definition
#  -----------------------------------------------------------------------------------------------------------------

def FindDefinition(word):
    txt="Shall I search for the definition of  \""+ word +"\"?\n"
    return txt

def AskDefinition(word):
    txt="Do you want to give your own definition for  \""+ word +"\"?\n"
    return txt

def YourDefinition(word):
    txt="What is your definition of  \""+ word +"\"?\n"
    return txt

def KeepWord(word):
    txt="Shall I keep  \"" + word + "\" without a definition?\n"
    txt+="If the answer is negative then the ontology will not keep this word.\n"
    return txt

def keepProperty(property):
    return "Should I keep the \""+property+"\""
#  -----------------------------------------------------------------------------------------------------------------
#                                        search Ontology talks
#  -----------------------------------------------------------------------------------------------------------------

def termFoundNoDescription(term,ontology):
    txt="The Ontology \""+ontology+"\" has no description for \""+term+"\".\n"
    txt+="Should I keep this ontology without a description?\n"
    txt+="If the answer is negative then this Ontology will be discarded and another Ontology will be searched.\n"
    return txt

def termKeepCategories(term,find):
    txt="Shall I keep the "+find+" of \""+term+"\"?\n"
    return txt

def termKeepTheCategoryWithDescription(term,category,description,ontology,find):
    txt="The Ontology \""+ontology+"\" has \""+category+"\" as "+find+" of \""+term+"\" with the description:\n"
    txt+=description+"\n"
    txt+="Shall I keep this?\n"
    return txt

def termKeepTheCategoryWithoutDescription(term,category,ontology,find):
    txt="The Ontology \""+ontology+"\" has \""+category+"\" as "+find+" of \""+term+"\" without a description.\n"
    txt+="Shall I keep this?\n"
    return txt


def termNoCategoryFound(term,ontology,find):
    txt="The ontology \""+ontology+"\" has no "+find+" for \""+term+"\".\n\n"
    return txt


def termFoundDescription(term,description,ontology):
    txt="The Ontology \""+ontology+"\" has the following description for \""+term+"\":\n"
    txt+=description+"\n"
    txt+="Shall I keep this ontology with a description\n"
    txt+="If the answer is negative then this Ontology will be discarded and another Ontology will be searched.\n"
    return txt

def seen5(term,find):
    txt="You have seen 5 "+ find +" of \""+term+"\"\n Do you want to see more?\n"
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
