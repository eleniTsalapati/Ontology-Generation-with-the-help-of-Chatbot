from tkinter.tix import Tree
import modules.chatbotTalks as talk
import modules.chatbotHears as hear

def questionWithYesOrNo(ui,txt):
    answer=0
    # do the question here
    ui.changeMessage(txt)

    while answer==0 :

        # get answer
        answerUI=ui.hearTrueOrFalse()
        answer=hear.GetTrueOrFalse(answerUI)

        # not correct answer
        if answer==0:
            ui.rememberOneTime(txt)
            ui.changeMessage(talk.CouldNotUnderstand())

    return answer

def convertStringToLowerTittle(txt):
    # convert the name to lower with capital case
    labels=txt.split()
    flag=False
    theLabel=""
    for label in labels:
        if flag==True:
            theLabel+=label.title()
        else:
            theLabel+=label.lower()
            flag=True
    return theLabel
    