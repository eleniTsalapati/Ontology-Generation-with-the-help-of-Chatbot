from tkinter.tix import Tree
import modules.chatbotTalks as talk
import modules.chatbotHears as hear
import owlready2

def questionWithYesOrNo(ui,txt):
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
    ui.changeMessage(txt)
    answerUI=ui.hear(1)
    return hear.FindNounsInDataBase(answerUI,data,ui)

def deleteData(data,ui,classes,relationships_others,ask=False):
    for i in classes: 
        if ask==True:
            ui.makeTables(data)
            if questionWithYesOrNo(ui,"Do you want to destroy\""+i+"\"?")==False:
                continue
        temp=list(data[1].keys())
        if i in data[0].keys():
            owlready2.destroy_entity(data[0][i][0])
            del data[0][i]
            for j in temp:
                if j in data[1].keys():
                    flag=False
                    for item in data[1][j][1]:
                        if item==i:
                            flag=True
                    if data[1][j][2]==i:
                        flag=True
                    if flag==True:
                        owlready2.destroy_entity(data[1][j][0])
                        del data[1][j]
            ui.updateTable(data)
                        
    for j in relationships_others:
        if ask==True:
            if questionWithYesOrNo(ui,"Do you want to destroy\""+j+"\"?")==False:
                continue
        if j in data[1].keys():
            owlready2.destroy_entity(data[1][j][0])
            del data[1][j]
            ui.updateTable(data)