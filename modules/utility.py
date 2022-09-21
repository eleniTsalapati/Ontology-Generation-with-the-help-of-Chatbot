from tkinter.tix import Tree
import modules.chatbotTalks as talk
import modules.chatbotHears as hear

def question_with_yes_or_No(ui,question):
    answer=0
    # do the question here
    ui.changeMessage(question())

    while answer==0 :

        # get answer
        answerUI=ui.hearTrueOrFalse()
        answer=hear.GetTrueOrFalse(answerUI)

        # not correct answer
        if answer==0:
            ui.rememberOneTime(question())
            ui.changeMessage(talk.CouldNotUnderstand())

    return answer


def question_arg1_with_yes_or_No(ui,question,arg1):
    answer=0

    # do the question here
    ui.changeMessage(question(arg1))

    while answer==0 :

        # get answer
        answerUI=ui.hearTrueOrFalse()
        answer=hear.GetTrueOrFalse(answerUI)

        if answer==0:
            ui.rememberOneTime(question(arg1))
            ui.changeMessage(talk.CouldNotUnderstand())

    return answer

def question_arg2_with_yes_or_No(ui,question,arg1,arg2):
    answer=0
    # do the question here
    ui.changeMessage(question(arg1,arg2))

    while answer==0 :
        
        

        # get answer
        answerUI=ui.hearTrueOrFalse()
        answer=hear.GetTrueOrFalse(answerUI)
    
        # not correct answer
        if answer==0:
            ui.rememberOneTime(question(arg1,arg2))
            ui.changeMessage(talk.CouldNotUnderstand())

    return answer

def question_arg3_with_yes_or_No(ui,question,arg1,arg2,arg3):
    answer=0
    
    # do the question here
    ui.changeMessage(question(arg1,arg2,arg3))

    while answer==0 :
        
        # get answer
        answerUI=ui.hearTrueOrFalse()
        answer=hear.GetTrueOrFalse(answerUI)
        
        # not correct answer
        if answer==0:
            ui.rememberOneTime(question(arg1,arg2,arg3))
            ui.changeMessage(talk.CouldNotUnderstand())

    return answer


def question_arg4_with_yes_or_No(ui,question,arg1,arg2,arg3,arg4):
    answer=0

    # do the question here
    ui.changeMessage(question(arg1,arg2,arg3,arg4))
    while answer==0 :
                
        # get answer
        answerUI=ui.hearTrueOrFalse()
        answer=hear.GetTrueOrFalse(answerUI)

        # not correct answer
        if answer==0:
            ui.rememberOneTime(question(arg1,arg2,arg3,arg4))
            ui.changeMessage(talk.CouldNotUnderstand())
        
    return answer