def Welcome():
    print("Welcome User!")
    print("This Chatbot is made to create an Ontology.")
    print("I will ask you questions about the ontology and you have to answer them.")
    print("Lets start!!")
    print()

def askTheFile():
    print("In which file shall I save the ontology?")
    print("IMPORTANT: If the file path is local then it has to begin with file://")
    print("           If the file path is digital then it has to begin with http://")

def GetOntology():
    print("From which file do you want the ontology to be saved?")
    
def FirstQuestion():
    print("What questions do you want your ontology to be able to answer?")

def CouldNotUnderstand():
    print("Sorry but I could not understand your answer.")

def AskDeffinition(word):
    print("Do you want to give your own definition for the word \""+ word +"\"?")

def YourDefinition(word):
    print("What is your definition for the word \""+ word +"\"?")

def FindDefinition(word):
    print("Shall I search for the definition of the word \""+ word +"\"?")

def KeepWord(word):
    print("Shall I keep the word \"" + word + "\" without a definion?")
    print("If the answer is negative then the ontology will not keep this word.")

def AskDiffrentTypes(word):
    print("Are there different types of the word \""+ word +"\"?")

def GetDiffrentTypes(word):
    print("Enumerate all different types of the word \""+ word +"\".")

# do it until all the objects have the questions
# What questions do you want your ontology to be able to answer with the object