from cgitb import reset
from re import sub
import modules.chatbotTalks as talk
import modules.ontologyManager as manager
from modules.dialogOptions import RadioDialog 

def checkInheritance(word,parent,ui):
    selected_option=None
    while(selected_option==None):
        # check if there is a parent to check for the inheritance
        if parent == None:
            return -1

        options=[]
        # check if the inheritance is correct
        options.append(talk.ontoCheck(parent,word))
        # check IDENTITY
        options.append(talk.identityComponentOf(parent,word))
        options.append(talk.identityComponentOf(word,parent))
        # check UNITY
        options.append(talk.unityComposedOf(parent,word))
        options.append(talk.unityComposedOf(word,parent))
        # None of the above
        options.append("None of the above")

        dialog=RadioDialog(ui,options,talk.InheritanceHeader(word))
        selected_option = dialog.run()
        if selected_option==None:
            ui.error("No option was selected. There has to be an option")
        else:
            # there is a parent and there is wrong with the inheritance
            if selected_option==talk.ontoCheck(parent,word):        
                return 0
            elif selected_option==talk.identityComponentOf(parent,word):
                return 1
            elif selected_option==talk.identityComponentOf(word,parent):
                return 2
            elif selected_option==talk.unityComposedOf(parent,word):
                return 3
            elif selected_option==talk.unityComposedOf(word,parent):
                return 4
            else:    
                return 5

def addInheritance(noun,parent,ui):
    # so check for the inheritance
    keepParent=[]
    keepRelation=[]
    if parent!=None:
        for theParent in parent:
            result=checkInheritance(noun,theParent,ui)
            if result==0:
                keepParent.append(theParent)
            elif result==1:
                relation=theParent.title()+"_ComponentOf_"+noun.title()
                keepRelation.append((relation,theParent,noun))
            elif result==2:
                relation=noun.title()+"_ComponentOf_"+theParent.title()
                keepRelation.append((relation,noun,theParent))
            elif result==3:
                relation=theParent.title()+"_ComposedOf_"+noun.title()
                keepRelation.append((relation,theParent,noun))                
            elif result==4:
                relation=noun.title()+"_ComposedOf_"+theParent.title()
                keepRelation.append((relation,noun,theParent))
    
    # add parents
    for theParent in keepParent:        
        manager.addParent(ui.data[2],ui.data[0][noun][0],ui.data[0][theParent][0],ui)
        ui.data[0][noun][2].append(theParent)
        ui.AddToTableParent(noun,theParent)
        ui.data[0][noun][2].append(theParent)

    # add relations
    for relation,object1,object2 in keepRelation:
        createRelation(ui.data,ui,object1,relation,object2)

    return True

def createNoun(noun,parent,ui,moreGeneralized=True):
    ui.moreGeneralized=moreGeneralized
    # check if the word is in data base
    for word in ui.data[0].keys():
        if noun.lower()==word.lower():
            ui.rememberOneTime("The word \""+noun+"\" is already in the dataBase\n")
            ui.taskNouns-=1
            if ui.whichTask=="Sentence":
                ui.checkTaskAddTerm()
            elif ui.whichTask=="Narrow":
                ui.checkTaskNarrow_Broaden()
            elif ui.whichTask=="Broaden":
                ui.checkTaskNarrow_Broaden()
            return 
    ui.search()


def createRelation(data,ui,obj1,relation,obj2):
    # mark as used
    data[0][obj1][3]=1
    data[0][obj2][3]=1

    if relation not in data[1].keys():
        # create the relationship
        data[1][relation]=[manager.ConnectObjects(data[2],relation,data[0][obj1][0],data[0][obj2][0],ui),[obj1],relation,obj2]
        ui.AddToTableRelationship(obj1,relation,obj2)
    else:
        manager.AddConnection(data[2],data[1][relation][0],data[0][obj1][0],ui)
        data[1][relation][1].append(obj1)
        ui.AddToTableRelationship(data[1][relation][0],relation,data[1][relation][1][-1])

