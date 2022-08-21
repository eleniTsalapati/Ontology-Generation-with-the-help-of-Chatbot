from tkinter.tix import Tree
import modules.chatbotTalks as talk
import modules.chatbotHears as hear

def question_with_yes_or_No(ui,question):
    answer=0
    flag=False
    while answer==0 :
        # do the question here
        if flag==True:
            ui.changeMessage(talk.CouldNotUnderstand(question()))
        else:
            ui.changeMessage(question())
            flag=True

        # get answer
        answerUI=ui.hearTrueOrFalse()
        answer=hear.GetTrueOrFalse(answerUI)

    return answer


def question_arg1_with_yes_or_No(ui,question,arg1):
    answer=0
    flag=True
    while answer==0 :
        # do the question here
        if flag==False:
            ui.changeMessage(talk.CouldNotUnderstand(question(arg1)))
        else:
            ui.changeMessage(question(arg1))
            flag=True

        # get answer
        answerUI=ui.hearTrueOrFalse()
        answer=hear.GetTrueOrFalse(answerUI)

    return answer

def question_arg2_with_yes_or_No(ui,question,arg1,arg2):
    answer=0
    flag=False

    while answer==0 :
        
        
        # do the question here
        if flag==True:
            ui.changeMessage(talk.CouldNotUnderstand(question(arg1,arg2)))
        else:
            ui.changeMessage(question(arg1,arg2))
            flag=True

        # get answer
        answerUI=ui.hearTrueOrFalse()
        answer=hear.GetTrueOrFalse(answerUI)

    return answer

def question_arg3_with_yes_or_No(ui,question,arg1,arg2,arg3):
    answer=0
    flag=False

    while answer==0 :
        
        
        # do the question here
        if flag==True:
            ui.changeMessage(talk.CouldNotUnderstand(question(arg1,arg2,arg3)))
        else:
            ui.changeMessage(question(arg1,arg2,arg3))
            flag=True

        # get answer
        answerUI=ui.hearTrueOrFalse()
        answer=hear.GetTrueOrFalse(answerUI)

    return answer


def question_arg4_with_yes_or_No(question,arg1,arg2,arg3,arg4,ui):
    answer=0
    flag=False

    while answer==0 :
        
        
        # do the question here
        if flag==True:
            ui.changeMessage(talk.CouldNotUnderstand(question(arg1,arg2,arg3,arg4)))
        else:
            ui.changeMessage(question(arg1,arg2,arg3,arg4))
            flag=True

        # get answer
        answerUI=ui.hearTrueOrFalse()
        answer=hear.GetTrueOrFalse(answerUI)

    return answer