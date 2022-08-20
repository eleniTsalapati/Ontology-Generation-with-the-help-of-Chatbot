import modules.chatbotTalks as talk
import modules.chatbotHears as hear

def question_Noun_with_yes_or_No(question,noun):
    answer=0
    while answer==0 :
        # do the question here
        question(noun)
        
        answer=hear.GetTrueOrFalse()

        # the answer is not positive or negative
        if answer==0:
            talk.CouldNotUnderstand()
    return answer

def question_with_yes_or_No(question):
    answer=0
    while answer==0 :
        # do the question here
        question()

        answer=hear.GetTrueOrFalse()

        # the answer is not positive or negative
        if answer==0:
            talk.CouldNotUnderstand()
    return answer
