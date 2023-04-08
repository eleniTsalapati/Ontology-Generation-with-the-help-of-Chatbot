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
    txt+="In which file shall I save the ontology?"
    return txt
    
def Menu():
    txt="Your Ontology has been saved. Now you can choose 1 from 4 options.\n\t"
    txt+="You can give: Competency Question, Narrow a term, Broaden a term, Delete a term."
    return txt

def Help():
    # Competency Question
    txt="To give a COMPETENCY QUESTION you have to put your answer in the area bellow and then press the button.\n\t"
    txt+="If you have a lot of nouns, then you need to have underscore \"_\" in between the nouns. \n\t"
    txt+="For example: Mitigation_Action and NOT Mitigation action\n\n\t"
    txt+="Please be careful with the grammar(the articles), syntax of the answer as it will affect it.\n\t"
    txt+="Recognize: A cat eats fishes, Cats eat the fish\n\t"
    txt+="Not Recognize: Cat eat fish\n\n\t"
    
    # Narrow term
    txt+="To NARROW a term, double click the term from the left table which you want to be narrowed and then click the button.\n\t"
    txt+="Important. The term has to be shown in the field down, so the button can be pressed.\n\n\t"

    # Broaden term
    txt+="To BROADEN a term, double click the term from the left table which you want to be broaden and then click the button.\n\t"
    txt+="Important. The term has to be shown in the field down, so the button can be pressed.\n\n\t"

    # Delete term
    txt+="To DELETE a term, double click the term from the left table which you want to be deleted and then click the button.\n\t"
    txt+="Important. The term has to be shown in the field down, so the button can be pressed."
    return txt

def CouldNotUnderstand():
    txt="\n\nSorry but I could not understand your answer.\n\n"
    return txt

#  -----------------------------------------------------------------------------------------------------------------
#                                        Definition
#  -----------------------------------------------------------------------------------------------------------------

def FindDefinition(word):
    txt="What should I do with the definition of \""+ word +"\"? Select one option.\n"
    return txt

def GiveDefinition(word):
    return "What should be the definition of  \""+ word +"\"? Put your answer in the text field and press enter.\n"

def KeepWithoutDefinition(word):
    return "I will keep the \""+word+"\" without any definition."

def DoNotKeep(word):
    return "I will not keep the \""+word+"\"."

#  -----------------------------------------------------------------------------------------------------------------
#                                        search Ontology talks
#  -----------------------------------------------------------------------------------------------------------------

def FoundOntology(ontology,description):
    txt="The Ontology \""+ontology+"\" was found with description:\n"
    txt+=description+"\n"
    return txt

def ChooseParent_Child(term,description):
    return "\""+term+"\" with description:\n"+description+"\n"

def termNoCategoryFound(term,ontology,type):
    return "In the \""+ontology+"\" for the \""+term+"\" no \""+type+"\" was found." 

#  -----------------------------------------------------------------------------------------------------------------
#                                        Header
#  -----------------------------------------------------------------------------------------------------------------

def InheritanceHeader(term):
    return "Which from the following is true for \""+term+"\"."

def ExternalOntologyHeader(term):
    return "Which external ontology do you want to keep for \""+term+"\"."

def ChildParentExternalHeader(term,find):
    return "Which term do you want to keep as "+find+" for \""+term+"\"."
#  -----------------------------------------------------------------------------------------------------------------
#                                        Narrow
#  -----------------------------------------------------------------------------------------------------------------

def whatToNarrow(term):
    return "With what terms should \""+term+"\" be narrowed? Select from the table or add your own term and then press enter."

#  -----------------------------------------------------------------------------------------------------------------
#                                        Broaden
#  -----------------------------------------------------------------------------------------------------------------

def whatToBroaden(term):
    return "With what terms should \""+term+"\" be broaden? Select from the table or add your own term and then press enter."

#  -----------------------------------------------------------------------------------------------------------------
#                                        Destroy
#  -----------------------------------------------------------------------------------------------------------------

def whatToDestroy(term):
    return "Do you want to Destroy \""+term+"\"?"


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
