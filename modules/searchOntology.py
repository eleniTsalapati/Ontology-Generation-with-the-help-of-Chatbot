import requests
import modules.chatbotTalks as talk
import modules.chatbotHears as hear
import modules.utility as utility

def Ontology_Children(term,current,ui):
    child_url="https://www.ebi.ac.uk/ols/api/ontologies/"+current["ontology_name"]+"/children?id="+current["obo_id"]
    response = requests.get(child_url)
    children=response.json()
    keepChildren=[]
    if children["page"]["totalElements"]==0:
        ui.rememberOneTime(talk.termNoKidFound(term,current["ontology_name"]))
        return []
    for child in children['_embedded']['terms']:
        
        answer=0
        while answer==0 :
            if "description" in child.keys() and child["description"]!=[]:
                utility.question_arg4_with_yes_or_No(ui,talk.termKeepTheKidWithDescription,term,child["label"],child["description"][0],current["ontology_name"])
            else:
                utility.question_arg3_with_yes_or_No(ui,talk.termKeepTheKidWithoutDescription,term,child["label"],current["ontology_name"])
        
        if answer==1:
            if "description" in child.keys() and child["description"]!=[]:
                keepChildren.append((child["label"],child["description"][0],current["ontology_name"]))
            else:
                keepChildren.append((child["label"],"",current["ontology_name"]))
    return keepChildren

def handleOntology(term,current,ui):
    if "description" not in  current.keys()  or current['description']==[]:
        answer=utility.question_arg3_with_yes_or_No(ui,talk.termFoundNoDescription,term,current["ontology_name"])        

        if answer==1:
            utility.question_arg1_with_yes_or_No(ui,talk.termKeepKids,term)

            if answer==1:
                children=Ontology_Children(term,current,ui)
                return ('',current["ontology_name"],children)
            else:
                return ('',current["ontology_name"],None)
    else:
        description=current["description"][0]
        
        answer=utility.question_arg3_with_yes_or_No(ui,talk.termFoundDescription,term,description,current["ontology_name"])        
    
        if answer==1:
            utility.question_arg1_with_yes_or_No(ui,talk.termKeepKids,term)
            if answer==1:
                children=Ontology_Children(term,current,ui)
                return (description,current["ontology_name"],children)
            else:
                return (description,current["ontology_name"],None)
    return (None,None,None)

def searchForTerm(term,ui):
    
    search_url="http://www.ebi.ac.uk/ols/api/search?q="+term
    response = requests.get(search_url)
    searchAnswer=response.json()
    flag=True
    previous=None
    for count in range(5):
        if count == searchAnswer['response']['numFound']:
            break

        current=searchAnswer['response']['docs'][count]
        if current["label"].lower() == term :
            previous=searchAnswer['response']['docs'][count]
            (description,name,kids) =handleOntology(term,current,ui)
            if description !=None:
                return (description,name,kids)

    if flag:
        ui.rememberOneTime("I have not found an ontology with that label!\n")
        if previous!=None:
            ui.rememberOneTime("I remember the previous ontology that I found.\n\n")
            return handleOntology(term,previous,ui)

    return (None,None,None)
