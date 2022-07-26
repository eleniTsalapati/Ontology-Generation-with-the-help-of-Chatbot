def GetOntology():
    print("From which file do you want the ontology to be saved?")
    
def FirstQuestion():
    print("What questions do you want your ontology to be able to answer?")


# Is there a definition
# If yes we keep it and we get definition
# If not then we ask if we want it without definition or we should change the word or delete it.

def GiveDeffinition(name):
    print("What is a "+name+"?")

def AskDiffrentTypes(name):
    print("Are there different types of "+name+"?")

def GetDiffrentTypes(name):
    print("Enumerate all different types of "+name+".")

# do it until all the objects have the questions
# What questions do you want your ontology to be able to answer with the object