from cgitb import reset
from re import sub
import modules.chatbotTalks as talk
import modules.ontologyManager as manager
import modules.chatbotHears as hear
import modules.searchOntology as search
import modules.utility as utility

def checkInheritance(word,parent,ui):
    # check if there is a parent to check for the inheritance
    if parent == None:
        return -1

    # check if the inheritance is correct
    answer=utility.questionWithYesOrNo(ui,talk.ontoCheck(parent,word))
    
    # there is a parent and there is wrong with the inheritance
    if answer==-1:        
        # check IDENTITY
        answer=utility.questionWithYesOrNo(ui,talk.identityComponentOf(parent,word))
        if answer==1:
            return 1
        else:
            ui.rememberOneTime("Ok now something new.\n")
            answer=utility.questionWithYesOrNo(ui,talk.identityComponentOf(word,parent))
            if answer==1:
                return 2
            else:
                # check UNITY
                answer=utility.questionWithYesOrNo(ui,talk.unityComposedOf(parent,word))
                if answer==1:
                    return 3
                else:
                    ui.rememberOneTime("Ok now something new.\n")
                    answer=utility.questionWithYesOrNo(ui,talk.unityComposedOf(word,parent))
                    if answer==1:
                        return 4
                    else:    
                        ui.rememberOneTime("I cannot understand how the connection goes so I will not use this connection.\n")
                        ui.rememberOneTime("Please fix the connection between \""+parent+"\" - \""+word+"\"")
                        return 5
    else:
        return 0

def createNoun(noun,parent,data,ui,moreGeneralized=True):
    # check if the word is in data base
    for word in data[0].keys():
        if noun==word.lower():
            ui.rememberOneTime("The word \""+noun+"\" is already in the dataBase\n")
            return

    ui.rememberTableOnce()
    answer= utility.questionWithYesOrNo(ui,"Shall I keep \""+noun+"\"\n")
    if answer==-1:
        return

    # so check for the inheritance
    keepParent=[]
    keepRelation=[]
    if parent!=None:
        for theParent in parent:
            result=checkInheritance(noun,theParent,ui)
            if result==0:
                keepParent.append(theParent)
            elif result==1:
                relation="componentOf"+noun.title()
                keepRelation.append(relation,theParent,noun)
            elif result==2:
                relation="componentOf"+noun.title()
                keepRelation.append(relation,noun,theParent)
            elif result==3:
                relation="composedOf"+noun.title()
                keepRelation.append(relation,theParent,noun)                
            elif result==4:
                relation="composedOf"+noun.title()
                keepRelation.append(relation,noun,theParent)


    answer= utility.questionWithYesOrNo(ui,talk.FindDefinition(noun))
    found=False
    # The user wants to find the definition
    if answer==1:
        try:
            # search the definition
            found=search.searchForTerm(data,noun,parent,ui,moreGeneralized)            
        except:
            ui.rememberOneTime("There is an error with the code either because there is a bug or you do not have access to Internet\n")

    # if the search definition was not selected
    if  found!=True:
        # you have given a definition
        (definition,definedBy)=findYourDefinition(noun,ui)
        if definition==None:
            return 

        # create the object
        data[0][noun]=[manager.CreateObject(data[2],noun),noun,[],0]
         # add definition
        manager.Explanation(data[2],data[0][noun][0],definition,definedBy)
    
    # add parents
    for theParent in keepParent:        
        manager.addParent(data[2],data[0][noun][0],data[0][theParent][0])
        data[0][noun][2].append(theParent)
   
    # add relations
    for relation,object1,object2 in keepRelation:

        # one object was not kept
        if object1 not in data[0].keys() or object2 not in data[0].keys():
            ui.rememberOneTime("One object does not exist so \""+relation+"\" is not created\n")
            continue

        # mark as seen
        data[0][object1][3]=1
        data[0][object2][3]=1
        
        # create relation
        if relation not in data[1].keys():
            # create the relationship
            data[1][relation]=[manager.ConnectObjects(data[2],relation,data[0][object1][0],data[0][object2][0]),[object1],relation,object2]
        else:
            manager.AddConnection(data[2],data[1][relation][0],data[0][object1][0])
            data[1][relation][2].append(object1)


def findYourDefinition(noun,ui):

    # ask if the user want to give definition
    answer= utility.questionWithYesOrNo(ui,talk.AskDefinition(noun))

    # The user wants to give the definition
    if answer == 1:
        ui.changeMessage(talk.YourDefinition(noun))
        answerUI=ui.hear()
        definition=hear.GetDefinition(answerUI)
        definedBy="You"
    # The user wants to do something else
    else:
        # See if the user wants to keep without definition
        answer= utility.questionWithYesOrNo(ui,talk.KeepWord(noun))
        
        # The user wants to keep without definition
        if answer==1:
            definition=""
            definedBy=""
        # The user does not want to keep the word
        else:
            definition=None
            definedBy=None

    return (definition,definedBy)

def Sentence(data,ui):

    # See what the ontology should answer
    ui.changeMessage(talk.WhatOntologyToAnswer())
    answerUI=ui.hear()
    (nouns,relationships)=hear.WhatOntologyToAnswer(answerUI,ui)

    # For all the nouns that we have
    for noun in nouns.keys():
        parent=nouns[noun]

        # find the definition of the noun
        createNoun(noun,[parent],data,ui)


    # for all relationships
    for relation in relationships.keys():

        # if one object is not created then do not create the relationship
        obj1=relationships[relation][0]
        obj2=relationships[relation][1]

        # one object was not kept
        if obj1 not in data[0].keys() or obj2 not in data[0].keys():
            continue

        relation=relation+obj2.title()

        # mark as used
        data[0][obj1][3]=1
        data[0][obj2][3]=1

        if relation not in data[1].keys():
            # create the relationship
            data[1][relation]=[manager.ConnectObjects(data[2],relation,data[0][obj1][0],data[0][obj2][0]),[obj1],relation,obj2]
        else:
            manager.AddConnection(data[2],data[1][relation][0],data[0][obj1][0])
            data[1][relation][1].append(obj1)


def specialize(data,ui):
    ui.changeMessage("Which words from the dataBase do you want to specialize?")
    answerUI=ui.hear()
    nouns=hear.FindNounsInDataBase(answerUI,data,ui)
    for noun in nouns:        
        ui.rememberTableOnce()
        ui.changeMessage(talk.GetDifferentTypes(noun))
        answerUI=ui.hear()
        types=hear.GetNouns(answerUI,ui)

        # for each type from the different types 
        for type in types:            
            createNoun(type,[noun],data,ui,False)

def generalized(data,ui):
    ui.changeMessage("Which word do you want to add?")
    answerUI=ui.hear()
    nouns=hear.GetNouns(answerUI,data,ui)
    for noun in nouns:        
        ui.rememberTableOnce()
        ui.changeMessage("Which words from DataBase do you want to be categorized as generalized with the word\""+noun+"\"\n")
        answerUI=ui.hear()
        parents=hear.FindNounsInDataBase(answerUI,ui)
        createNoun(noun,parents,data,ui,False)
