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

ui.rememberOneTime("I have loaded the file \""+answer+"\"\n\n")
data.append(manager.LoadOntology(answer))
manager.addData(data[2],data)

while(True):
    ui.makeTables(data)
    answer= utility.questionWithYesOrNo(ui,talk.MoreOntology())

    if answer == 1:
        ui.rememberTableOnce()
        Sentence(data,ui)
        continue

    ui.rememberTableOnce()
    answer= utility.questionWithYesOrNo(ui,talk.EnumerateSpecialization())
    if answer == 1:
        ui.rememberTableOnce()
        specialize(data,ui)
        continue

    ui.rememberTableOnce()
    answer= utility.questionWithYesOrNo(ui,talk.EnumerateGeneralization())
    if answer == 1:
        ui.rememberTableOnce()
        generalized(data,ui)
        continue

    break


# Save the ontology
manager.SaveOntology(data[2])

ui.close()
