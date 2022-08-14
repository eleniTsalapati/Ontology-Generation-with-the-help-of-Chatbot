from curses import noecho
import requests
import modules.chatbotTalks as talk
import modules.chatbotHears as hear

def Ontology_Children(term,current):
    child_url="https://www.ebi.ac.uk/ols/api/ontologies/"+current["ontology_name"]+"/children?id="+current["obo_id"]
    response = requests.get(child_url)
    children=response.json()
    keepChildren=[]
    if children["page"]["totalElements"]==0:
        talk.termNoKidFound(term,current["ontology_name"])
        return []
    for child in children['_embedded']['terms']:
        answer=0
        while answer==0 :
            if "description" in child.keys():
                talk.termKeepTheKidWithDescription(term,child["label"],child["description"][0],current["ontology_name"])
            else:
                talk.termKeepTheKidWithoutDescription(term,child["label"],current["ontology_name"])
            answer=hear.GetTrueOrFalse()
            if answer==0:
                talk.CouldNotUnderstand()
        if answer==1:
            if "description" in child.keys():
                keepChildren.append((child["label"],child["description"][0],current["ontology_name"]))
            else:
                keepChildren.append((child["label"],"",current["ontology_name"]))
    return keepChildren
        

def searchForTerm(term):
    
    search_url="http://www.ebi.ac.uk/ols/api/search?q="+term
    response = requests.get(search_url)
    searchAnswer=response.json()
    flag=True
    for count in range(5):
        if count == searchAnswer['response']['numFound']:
            break

        current=searchAnswer['response']['docs'][count]
        if current["label"].lower() == term :
            if "description" not in  current.keys():
                answer=0
                while answer==0 :
                    talk.termFoundNoDescription(term,current["ontology_name"])
                    answer=hear.GetTrueOrFalse()
                    if answer==0:
                        talk.CouldNotUnderstand()
                if answer==1:
                    answer=0
                    while answer==0 :
                        talk.termKeepKids(term)
                        answer=hear.GetTrueOrFalse()
                        if answer==0:
                            talk.CouldNotUnderstand()
                    if answer==1:
                        children=Ontology_Children(term,current)
                        return ('',current["ontology_name"],children)
                    else:
                        return ('',current["ontology_name"],None)
            else:
                answer=0
                description=current["description"][0]
                while answer==0 :
                    talk.termFoundDescription(term,description,current["ontology_name"])
                    answer=hear.GetTrueOrFalse()
                    if answer==0:
                        talk.CouldNotUnderstand()
                if answer==1:
                    answer=0
                    while answer==0 :
                        talk.termKeepKids(term)
                        answer=hear.GetTrueOrFalse()
                        if answer==0:
                            talk.CouldNotUnderstand()
                    if answer==1:
                        children=Ontology_Children(term,current)
                        return (description,current["ontology_name"],children)
                    else:
                        return (description,current["ontology_name"],None)
    if flag:
        print("I have not found an ontology with that label!")
    return (None,None,None)