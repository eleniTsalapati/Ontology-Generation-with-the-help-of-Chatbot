from tkinter.messagebox import YES
import requests
import modules.ontologyManager as manager
import modules.chatbotTalks as talk
import modules.utility as utility
import urllib.parse
from modules.dialogOptions import RadioDialog,CheckDialog

def acceptSearch(term,ontology,obo_id,find,data,ui):
    # get api answer
    url="https://www.ebi.ac.uk/ols/api/ontologies/"+ontology+"/"+find+"?id="+obo_id
    response = requests.get(url)
    dataBase=response.json()
    label=""
    text=""
    if find=="children":
        text="specialization"
    else:
        text="generalization"
    # for each data
    options=[]
    for word in dataBase['_embedded']['terms']:
        description=""
        if "description" in word.keys() and word["description"]!=[]:
            description=word["description"][0]
        # we want to keep word
        label=utility.convertStringToLowerTittle(word["label"])
        options.append(talk.ChooseParent_Child(label,description))
    dialog=None
    if find=="children":
        dialog=CheckDialog(ui,options,text,term)
    else:
        dialog=CheckDialog(ui,options,text,term)
    selectedTerms = dialog.run()
    if selectedTerms==[]:
        ui.addTextChatBot("No "+find+" was selected")
    else:
        text="Selected:\n"
        for selected in selectedTerms:
            text+=selected+"\n"
        ui.addTextUser(text)
        for selected in selectedTerms:
            label=selected.split("\"")[1]
            # crete object
            # create local
            external=ontology+":"+label
            data[0][label]=[manager.CreateObject(data[2],label,ui),label,[external],0]
            ui.AddToTableTerm(label)

            # create external
            data[0][external]=[manager.CreateObject(data[2],external,ui),external,[],0]
            data[0][external][0].iri=word["iri"]
            manager.addParent(data[2],data[0][label][0],data[0][external][0],ui)
            ui.AddToTableTerm(external)
            
            # add description
            if "description" in word.keys() and word["description"]!=[]:
                manager.Explanation(data[2],data[0][external][0],word["description"][0],ontology,ui)
            else:
                manager.Explanation(data[2],data[0][external][0],"",ontology,ui)
            
            
            # add the necessary data
            if find=="parents":
                # local
                manager.addParent(data[2],data[0][term][0],data[0][label][0],ui)
                data[0][term][2].append(label)                            
                # external
                external2=ontology+":"+term
                manager.addParent(data[2],data[0][external2][0],data[0][external][0],ui)
                data[0][external2][2].append(external)                            
            else:
                manager.addParent(data[2],data[0][label][0],data[0][term][0],ui)
                data[0][label][2].append(term)

                # external
                external2=ontology+":"+term
                manager.addParent(data[2],data[0][external][0],data[0][external2][0],ui)
                data[0][external][2].append(external2)                            

            # do recursive action
            if find=="children" and word["has_children"]==True:
                acceptSearch(label,ontology,word["obo_id"],find,data,ui)
            elif find=="parents" and word["is_root"]==False:
                acceptSearch(label,ontology,word["obo_id"],find,data,ui)

def handleOntology(data,term,parent,current,ui,moreGeneralize):
    description=""
    if "description" in  current.keys()  and current['description']!=[]:
        description=current["description"][0]
    # search the term to check for children and parents 
    text=urllib.parse.quote(current["iri"],safe='')
    text=urllib.parse.quote(text)
    search_url="http://www.ebi.ac.uk/ols/api/ontologies/"+current["ontology_name"]+"/terms/"+text
    response = requests.get(search_url)
    theResponse=response.json()

    # create local
    external=current["ontology_name"]+":"+term
    data[0][term]=[manager.CreateObject(data[2],term,ui),term,[external],0]
    ui.AddToTableTerm(term)

    # create external
    data[0][external]=[manager.CreateObject(data[2],external,ui),external,[],0]
    data[0][external][0].iri=current["iri"]
    manager.addParent(data[2],data[0][term][0],data[0][external][0],ui)
    ui.AddToTableTerm(external)

    manager.Explanation(data[2],data[0][external][0],description,current["ontology_name"],ui)

    # check if it can be generalized
    if ((parent==[] or parent==None) and theResponse["is_root"]==False and moreGeneralize==True):
        acceptSearch(term,current["ontology_name"],current["obo_id"],"parents",data,ui)
    elif(parent!=[] and parent!=None):
        ui.rememberOneTime("It is the root of your given ontology\n")
    else:
        ui.rememberOneTime("It is the root of the \""+current["ontology_name"]+"\"\n")


    # check for children
    if (theResponse["has_children"]==True):
        acceptSearch(term,current["ontology_name"],current["obo_id"],"children",data,ui)
    else:
        ui.rememberOneTime(talk.termNoCategoryFound(term,current["ontology_name"],"children"))

    
def searchForTerm(data,term,parent,ui,moreGeneralized):
    txt=""
    for theTerm in term.split("_"):
        if txt=="":
            txt=theTerm.lower()
        else:
            txt=txt+"+"+theTerm.lower()
    search_url="http://www.ebi.ac.uk/ols/api/search"
    response = requests.get(search_url+"?q="+txt)
    # check if there is ontology 
    if response.status_code%100 ==4 or response.status_code%100 ==5:
        ui.rememberOneTime("No ontology found\n")
        return (None,None,None)
    
    searchAnswer=response.json()
    txt=""
    for theTerm in term.split("_"):
        if txt=="":
            txt=theTerm.lower()
        else:
            txt=txt+" "+theTerm.lower()

    options=[]
    ontologies={}
    # look only the first 5 ontologies
    for count in range(5):
        if count == searchAnswer['response']['numFound']:
            break

        current=searchAnswer['response']['docs'][count]
        # check if it is the term you want
        if current["label"].lower() == txt :
            description="No description"
            if "description" in  current.keys()  and current['description']!=[]:
                description=current["description"][0]
            options.append(talk.FoundOntology(current["ontology_name"],description))
            ontologies[current["ontology_name"]]=current
    dialog = RadioDialog(ui,options,term)
    selected_option = dialog.run()
    if selected_option==None:
        ui.addTextChatBot("No External Ontology was selected")
    else:
        selectedOntology=selected_option.split("\"")[1]
        ui.addTextUser(selectedOntology)
        handleOntology(data,term,parent,ontologies[selectedOntology],ui,moreGeneralized)
        ui.taskNouns-=1
        ui.checkTask()
