import requests
import modules.chatbotTalks as talk
import modules.utility as utility

def Ontology_Children(term,current,ui):
    
    if "obo_id" not in current.keys():
        ui.rememberOneTime(talk.termNoSubcategoryFound(term,current["ontology_name"]))
        return []

    child_url="https://www.ebi.ac.uk/ols/api/ontologies/"+current["ontology_name"]+"/children?id="+current["obo_id"]
    print(child_url)
    response = requests.get(child_url)
    if response.status_code%100 ==4 or response.status_code%100 ==5:
        ui.rememberOneTime(talk.termNoSubcategoryFound(term,current["ontology_name"]))
        return []

    children=response.json()
    keepChildren=[]
    if children["page"]["totalElements"]==0:
        ui.rememberOneTime(talk.termNoSubcategoryFound(term,current["ontology_name"]))
        return []
    count=0
    mark=6
    for child in children['_embedded']['terms']:
        count+=1
        ui.rememberTableOnce()
        if count==mark:
            answer=utility.question_arg1_with_yes_or_No(ui,talk.seen5Sub,term)
            if answer==1:
                mark+=5
            else:
                break
        answer=0
        while answer==0 :
            if "description" in child.keys() and child["description"]!=[]:
                answer=utility.question_arg4_with_yes_or_No(ui,talk.termKeepTheSubcategoryWithDescription,term,child["label"],child["description"][0],current["ontology_name"])
            else:
                answer=utility.question_arg3_with_yes_or_No(ui,talk.termKeepTheSubcategoryWithoutDescription,term,child["label"],current["ontology_name"])
        
        if answer==1:
            labels=child["label"].split()
            flag=False
            theLabel=""
            for label in labels:
                if flag==True:
                    theLabel+=label.title()
                else:
                    theLabel+=label.lower()
                    flag=True
            if "description" in child.keys() and child["description"]!=[]:
                keepChildren.append((theLabel,child["description"][0],current["ontology_name"]))
            else:
                keepChildren.append((theLabel,"",current["ontology_name"]))
            ui.insertSubjectTable(theLabel,term)
    return keepChildren

def handleOntology(term,current,parent,ui):
    if "description" not in  current.keys()  or current['description']==[]:
        ui.rememberTableOnce()
        answer=utility.question_arg2_with_yes_or_No(ui,talk.termFoundNoDescription,term,current["ontology_name"])        

        if answer==1:
            print(current.keys())
            ui.rememberTableOnce()

            ui.insertSubjectTable(term,parent)
            answer=utility.question_arg1_with_yes_or_No(ui,talk.termKeepSubcategories,term)
            if answer==1:
                children=Ontology_Children(term,current,ui)
                return ('',current["ontology_name"],children)
            else:
                return ('',current["ontology_name"],None)
    else:
        description=current["description"][0]
        ui.rememberTableOnce()
        answer=utility.question_arg3_with_yes_or_No(ui,talk.termFoundDescription,term,description,current["ontology_name"])        
    
        if answer==1:
            ui.rememberTableOnce()
            ui.insertSubjectTable(term,parent)
            answer=utility.question_arg1_with_yes_or_No(ui,talk.termKeepSubcategories,term)
            if answer==1:
                children=Ontology_Children(term,current,ui)
                return (description,current["ontology_name"],children)
            else:
                return (description,current["ontology_name"],None)
    return (None,None,None)

def searchForTerm(term,parent,ui):
    search_url="http://www.ebi.ac.uk/ols/api/search?q="+term
    response = requests.get(search_url)
    if response.status_code%100 ==4 or response.status_code%100 ==5:
        ui.rememberOneTime("No ontology found\n")
        return (None,None,None)
    
    searchAnswer=response.json()
    flag=True
    previous=None
    for count in range(5):
        if count == searchAnswer['response']['numFound']:
            break

        current=searchAnswer['response']['docs'][count]
        if current["label"].lower() == term :
            previous=searchAnswer['response']['docs'][count]
            (description,name,subcategories) =handleOntology(term,current,parent,ui)
            if description !=None:
                return (description,name,subcategories)

    if flag:
        if count == 0 :
            ui.rememberOneTime("I have not found an ontology with that label!\n")
        elif count<5:
            ui.rememberOneTime("I do not have anymore ontologies to shown\n")
        else:
            ui.rememberOneTime("I have shown you 5 ontologies. Due to that I will not show any more\n")
        if previous!=None:
            ui.rememberOneTime("I remember the previous ontology that I found.\n\n")
            return handleOntology(term,previous,parent,ui)

    return (None,None,None)
