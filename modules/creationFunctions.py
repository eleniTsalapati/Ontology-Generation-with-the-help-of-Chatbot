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
        options.append(talk.hasPart(parent,word))
        options.append(talk.hasPart(word,parent))
        # check UNITY
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
            elif selected_option==talk.hasPart(parent,word):
                return 1
            elif selected_option==talk.hasPart(word,parent):
                return 2
            else:    
                return 3

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
                relation="HasPart"
                keepRelation.append((relation,theParent,noun))
            elif result==2:
                relation="HasPart"
                keepRelation.append((relation,noun,theParent))
    
    # add parents
    for theParent in keepParent:        
        manager.addParent(ui.data[2],ui.data[0][noun][0],ui.data[0][theParent][0],ui)
        ui.data[0][noun][2].append(theParent)
        ui.AddToTableParent(noun,theParent)

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

    key=relation
    if key not in data[1].keys():
        # create the relationship
        data[1][key]=[manager.ConnectObjects(data[2],relation,data[0][obj1][0],data[0][obj2][0],ui),[obj1],relation,[obj2]]
        ui.AddToTableRelationship(key)
    else:
        manager.AddConnection(data[2],data[1][key][0],data[0][obj1][0],data[0][obj2][0],ui)
        if obj1 not in data[1][key][1]:
            data[1][key][1].append(obj1)
        if obj2 not in data[1][key][3]:
            data[1][key][3].append(obj2)
        ui.AddToTableRelationship(key)

