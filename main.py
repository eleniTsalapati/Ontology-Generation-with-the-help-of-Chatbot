from modules.UI import UI
import modules.chatbotTalks as talk
import modules.ontologyCreation as creation
import modules.chatbotHears as hear
import modules.searchOntology as search
import modules.utility as utility
from modules.mainFunctions import *

# -------------------------------------------------------
#                       main
# -------------------------------------------------------

# classes=[classesObj,classesRel]
# classesObj=[class,name,parent,foundOnline]
classes=[{},{}]
ui= UI()
seen=[]
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
ontology=creation.LoadOntology(answer)

creation.addData(ontology,classes)

ui.makeTablesClass(classes)
what_the_ontology_should_answer(ontology,classes,ui)

while(True):
    ui.makeTablesClass(classes)
    answer= utility.question_with_yes_or_No(ui,talk.MoreOntology)

    if answer == 1:
        ui.rememberTableOnce()
        what_the_ontology_should_answer(ontology,classes,ui)
        continue

    ui.rememberTableOnce()
    answer= utility.question_with_yes_or_No(ui,talk.EnumerateTheClasses)

    if answer == 1:
        ui.rememberTableOnce()
        more_types(ontology,classes,seen,ui)
        continue
    break

# Save the ontology
creation.SaveOntology(ontology)

ui.close()
