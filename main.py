from modules.UI import UI
import modules.chatbotTalks as talk
import modules.ontologyManager as manager
import modules.chatbotHears as hear
import modules.utility as utility
from modules.mainFunction import *

# -------------------------------------------------------
#                       main
# -------------------------------------------------------

# data=[dataObj,dataRel,ontology]
# dataObj=[class,name,parent,used/notUsed,external/or not]
# dataRel=[class,obj1name,obj2name]
data=[{},{}]
ui= UI()
# Welcome
ui.create()
# Load the ontology
answer = None
ui.changeMessage(talk.Welcome())
while answer == None:
    answerUI=ui.hear()
    answer=hear.thePath(answerUI)
    
    if answer==None:
        ui.rememberOneTime(talk.Welcome())
        ui.changeMessage(talk.CouldNotUnderstand())

path=answer
ui.rememberOneTime("I have loaded the file \""+answer+"\"\n\n")
data.append(manager.LoadOntology(path))
manager.addData(data[2],data)
answer=-1
while(answer!=3):
    ui.makeTables(data)

    ui.changeMessage("Your ontology has been saved.\nChoose one action from the buttons bellow!")
    manager.SaveOntology(data[2],path)
    answer=ui.hearMenu()
    
    if answer == 0:
        Sentence(data,ui)
    elif answer == 1:
        generalized(data,ui)
    elif answer == 2:
        specialize(data,ui)
    

# Save the ontology
manager.SaveOntology(data[2],path)
ui.close(path)
