import modules.chatbotTalks as talk
import owlready2
from modules.dialogOptions import CheckDialog
import modules.ontologyManager as manager

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

def removeFromRelationship(data,key,option,ui):
    flag=False
    flagDeleteAll=False
    for domain in data[1][key][1]:
        if option==domain:
            if len(data[1][key][1])==1:
                ui.addTextChatBot("No more terms in domain. Deleting the whole relationship.")
                owlready2.destroy_entity(data[1][key][0])
                del data[1][key]
                ui.RemoveRelationship(key)
                flagDeleteAll=True
            else:
                manager.RemoveDomain(data[2],data[1][key][0],data[0][domain][0],ui)
                data[1][key][1].remove(domain)
                ui.AddToTableRelationship(key)
                flag=True
            break
    if flagDeleteAll==True:
        return True
    if flag==True:
        return False
    for range in data[1][key][3]:
        if option==range:
            if len(data[1][key][3])==1:
                ui.addTextChatBot("No more terms in range. Deleting the whole relationship.")
                owlready2.destroy_entity(data[1][key][0])
                del data[1][key]
                flagDeleteAll=True
                ui.RemoveRelationship(key)
            else:
                manager.RemoveRange(data[2],data[1][key][0],data[0][range][0],ui)
                data[1][key][3].remove(range)
                ui.AddToTableRelationship(key)
                flag=True
            break
    if flagDeleteAll==True:
        return True
    return False


def deleteData(ui,terms,relationships_others,ask=False):
    options=terms
    data=ui.data
    if ask==True and terms!=[]:
        options=[]
        for i in terms:
            options.append(talk.whatToDestroy(i))
        options=CheckDialog(ui,options,"Are you sure you want to delete this items?").run()
        for i in options:
            ui.addTextUser(i)
    for i in options:     
        i=i.split("\"")[1]        
        temp=list(data[0].keys())
        if i in temp:
            for key in list(data[1].keys()):
                for item in data[1][key][1]:
                    if item==i:
                        break
                else:
                    for item in data[1][key][3]:
                        if item==i:
                            break
                    else:
                        continue
                removeFromRelationship(data,key,i,ui)
            owlready2.destroy_entity(data[0][i][0])
            del data[0][i]
            for j in list(data[0].keys()):
                if i in data[0][j][2]: 
                    data[0][j][2].remove(i)
            ui.RemoveTerm(i)

    options=relationships_others
    if ask==True and relationships_others!=[]:
        options=[]
        for i in relationships_others:
            options.append(talk.whatToDestroy(i))
        options=CheckDialog(ui,options,"What do you want to delete from this relationship?").run()
        for i in options:
            ui.addTextUser(i)


    for j in options:
        j=j.split("\"")[1]
        relation=j.split("_")
        key=None
        for i in relation:
            if i in data[1].keys():
                key=i
                break
        else:
            ui.rememberOneTime("No \""+j+"\" was found.")
            continue
        
        options=[]
        for i in relation:
            if i==key:
                options.append("Delete the whole relationship")
            elif i!="Or":
                options.append("Delete only the tern \""+i+"\" from the relationship")
        options=CheckDialog(ui,options,"Are you sure you want to delete this items?").run()
        if "Delete the whole relationship" in options:
            ui.addTextUser("Delete the whole relationship")
            owlready2.destroy_entity(data[1][key][0])
            del data[1][key]
            ui.RemoveRelationship(key)
        else:
            for option in options:
                option=option.split("\"")[1]
                ui.addTextUser(option)
                answer=removeFromRelationship(data,key,option,ui)
                if answer==True:
                    break


    
    ui.Menu()