from tkinter.tix import Tree
import modules.chatbotTalks as talk
import modules.chatbotHears as hear

def questionWithYesOrNo(ui,txt):
    answer=0
    # do the question here
    ui.changeMessage(txt)

    # get answer
    return ui.hearTrueOrFalse()

def convertStringToLowerTittle(txt):
    # convert the name to lower with capital case
    labels=txt.split()
    theLabel=""
    for label in labels:
        if theLabel=="":
            theLabel=label.lower()
        else:
            theLabel=theLabel+"_"+label.title()
    return theLabel
    
def FindNounsInDataBase(data,ui,txt):
    ui.makeTables(data)
    ui.changeMessage(txt)
    answerUI=ui.hear(1)
    return hear.FindNounsInDataBase(answerUI,data,ui)