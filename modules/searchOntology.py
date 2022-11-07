from tkinter.messagebox import YES
import requests
import modules.ontologyManager as manager
import modules.chatbotTalks as talk
import modules.utility as utility
import urllib.parse


def acceptSearch(term,ontology,obo_id,find,data,ui):
    # get api answer
    url="https://www.ebi.ac.uk/ols/api/ontologies/"+ontology+"/"+find+"?id="+obo_id
    response = requests.get(url)
    dataBase=response.json()
    mark=6
    count=0

    label=""

    if find=="children":
        text="specialization"
    else:
        text="generalization"
    # for each data
    for word in dataBase['_embedded']['terms']:
        count+=1
        # check if we have seen 5 subjects so to not see more
        if count==mark:
            answer=utility.questionWithYesOrNo(ui,talk.seen5(term,text))
            if answer==1:
                mark+=5
            else:
                break
        # check to see if you want the word
        answer=0
        if "description" in word.keys() and word["description"]!=[]:
            answer=utility.questionWithYesOrNo(ui,talk.termKeepTheCategoryWithDescription(term,word["label"],word["description"][0],ontology,find))
        else:
            answer=utility.questionWithYesOrNo(ui,talk.termKeepTheCategoryWithoutDescription(term,word["label"],ontology,find))
        
        # we want to keep word
        if answer==1:
            label=utility.convertStringToLowerTittle(word["label"])

            # crete object
            data[0][label]=[manager.CreateObject(data[2],label),label,[],0]
            ui.makeTables(data)

            data[0][label][0].iri=word["iri"]

            # add description
            if "description" in word.keys() and word["description"]!=[]:
                manager.Explanation(data[2],data[0][term][0],word["description"][0],ontology)
            else:
                manager.Explanation(data[2],data[0][term][0],"",ontology)
            
            
            # add the necessary data
            if find=="parents":
                manager.addParent(data[2],data[0][term][0],data[0][label][0])
                data[0][term][2].append(label)                            
            else:
                manager.addParent(data[2],data[0][label][0],data[0][term][0])
                data[0][label][2].append(term)

            # do recursive action
            if find=="children" and word["has_children"]==True:
                acceptSearch(label,ontology,word["obo_id"],find,data,ui)
            elif find=="parents" and word["is_root"]==False:
                acceptSearch(label,ontology,word["obo_id"],find,data,ui)

def handleOntology(data,term,parent,current,ui,moreGeneralize):
    # check if there is a description
    description=""
    if "description" in  current.keys()  and current['description']!=[]:
        description=current["description"][0]

    # ask if you want to keep it
    ui.makeTables(data)
    answer=utility.questionWithYesOrNo(ui,talk.termFoundNoDescription(term,current["ontology_name"]))        

    if answer==1:
        
        # search the term to check for children and parents 
        text=urllib.parse.quote(current["iri"],safe='')
        text=urllib.parse.quote(text)
        search_url="http://www.ebi.ac.uk/ols/api/ontologies/"+current["ontology_name"]+"/terms/"+text
        response = requests.get(search_url)
        theResponse=response.json()

        # create data
        data[0][term]=[manager.CreateObject(data[2],term),term,[],0]
        data[0][term][0].iri=current["iri"]

        manager.Explanation(data[2],data[0][term][0],description,current["ontology_name"])

        # check if it can be generalized
        if (parent==[] and theResponse["is_root"]==False and moreGeneralize==True):
            answer=utility.questionWithYesOrNo(ui,talk.termKeepCategories(term,"parents"))
            if answer==1:
                acceptSearch(term,current["ontology_name"],current["obo_id"],"parents",data,ui)
        elif(parent!=[]):
            ui.rememberOneTime("It is the root of your given ontology\n")
        else:
            ui.rememberOneTime("It is the root of the \""+current["ontology_name"]+"\"\n")

        ui.makeTables(data)

        # check for children
        if (theResponse["has_children"]==True):
            answer=utility.questionWithYesOrNo(ui,talk.termKeepCategories(term,"children"))
            if answer==1:
                acceptSearch(term,current["ontology_name"],current["obo_id"],"children",data,ui)
                return True
        else:
            ui.rememberOneTime(talk.termNoCategoryFound(term,current["ontology_name"],"children"))
        return True
    return False

    
def searchForTerm(data,term,parent,ui,moreGeneralized):
    txt=""
    for theTerm in term.split("_"):
        if txt=="":
            txt=theTerm.lower()
        else:
            txt=txt+"+"+theTerm.lower()
    search_url="http://www.ebi.ac.uk/ols/api/search"
    print(search_url+"?q="+txt)
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

    flag=True
    previous=None
    # look only the first 5 ontologies
    for count in range(5):
        if count == searchAnswer['response']['numFound']:
            break

        current=searchAnswer['response']['docs'][count]
        # check if it is the term you want
        if current["label"].lower() == txt :
            previous=searchAnswer['response']['docs'][count]
            # check if you want the this ontology
            used =handleOntology(data,term,parent,current,ui,moreGeneralized)
            if used == True:
                # you wanted the ontology so go back
                return True

    # checked the first 5 
    if flag:
        if count == 0 :
            ui.rememberOneTime("I have not found an ontology with that label!\n")
        elif count<5:
            ui.rememberOneTime("I do not have anymore ontologies to shown\n")
        else:
            ui.rememberOneTime("I have shown you 5 ontologies. Due to that I will not show any more\n")
        if previous!=None:
            ui.rememberOneTime("I remember the previous ontology that I found.\n\n")
            return handleOntology(data,term,parent,previous,ui,moreGeneralized)
    return False

