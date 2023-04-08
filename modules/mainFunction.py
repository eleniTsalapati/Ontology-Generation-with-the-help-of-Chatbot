from cgitb import reset
from re import sub
import modules.chatbotHears as hear
import modules.utility as utility


def Sentence(sentence,ui):
    # See what the ontology should answer
    (ui.nouns,ui.relationships)=hear.WhatOntologyToAnswer(sentence,ui)
    ui.taskNouns=len(ui.nouns.keys())
    ui.checkTaskAddTerm()

def narrow(parent,ui):
    ui.nouns,_=hear.FindNounsInDataBase(parent,ui)
    ui.taskNouns=len(ui.nouns)
    ui.checkTaskNarrow_Broaden()
    
def broaden(noun,ui):
    ui.nouns,_=hear.FindNounsInDataBase(noun,ui)
    ui.taskNouns=len(ui.nouns)
    ui.checkTaskNarrow_Broaden()

def destroy(text,ui):
    # find the classes and the relationships
    classes,relationships_others=hear.FindNounsInDataBase(text,ui)
    utility.deleteData(ui,classes,relationships_others,True)
    