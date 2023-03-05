from modules.UI import UI
import modules.chatbotTalks as talk
import modules.ontologyManager as manager
import modules.chatbotHears as hear
import modules.utility as utility
from modules.mainFunction import *
import modules.log as log
# -------------------------------------------------------
#                       main
# -------------------------------------------------------
# data=[dataObj,dataRel,ontology]
# dataObj=[class,name,parent,used/notUsed,external/or not, list with instances]
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
    if answer==None or (answer[:7]=="file://" and answer[7]!="/"):
        ui.give_back_browser_button()
        ui.rememberOneTime(talk.Welcome())
        txt="Be careful to add \"file://\"and then the correct path.\n"
        txt+="For example: file:///home/user/Desktop/file"
        ui.changeMessage(talk.CouldNotUnderstand()+txt)
        answer=None
path=answer
ui.rememberOneTime("I have loaded the file \""+answer+"\"\n\n")
data.append(manager.LoadOntology(path,ui))
manager.addData(data[2],data)
while(True):
    manager.SaveOntology(data[2],path,ui)

    ui.changeMessage("Your ontology has been saved.\nChoose one action from the buttons bellow!")
    ui.makeTables(data)

    answer=ui.hearMenu()
    
    if answer == "Sentence":
        Sentence(data,ui)
    elif answer == "Generalized":
        generalized(data,ui)
    elif answer == "Specialize":
        specialize(data,ui)
    elif answer == "Destroy Entity":
        destroy(data,ui)
    elif answer == "Exit":
        break  
    else:
        ui.rememberOneTime(talk.CouldNotUnderstand())
    

# Save the ontology
manager.SaveOntology(data[2],path,ui)
ui.close(path)
