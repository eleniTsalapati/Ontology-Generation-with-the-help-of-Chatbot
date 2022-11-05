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
# dataObj=[class,name,parent,used/notUsed]
# dataRel=[class,obj1name,obj2name]
print("!")
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
data.append(manager.LoadOntology(file))
manager.addData(data[2],data)
answer=-1
while(answer!=3):
    ui.makeTables(data)

    ui.changeMessage("Your ontology has been saved.\nChoose one action from the buttons bellow!")
    manager.SaveOntology(data[2])
    answer=ui.hearMenu()
    
    if answer == 0:
        ui.rememberTableOnce()
        Sentence(data,ui)
    elif answer == 1:
        ui.rememberTableOnce()
        generalized(data,ui)
    elif answer == 2:
        ui.rememberTableOnce()
        specialize(data,ui)
    

# Save the ontology
manager.SaveOntology(data[2])
ui.close(path)
