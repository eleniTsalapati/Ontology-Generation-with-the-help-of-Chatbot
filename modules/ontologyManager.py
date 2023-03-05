from owlready2 import *

def checkHttp(file):
    http="http://"
    # there is no room for http
    if len(file) <len(http):
        return False
    
    # check if all one of the letter in http is not inside file
    for i in range(len(http)):
        if file[i]!=http[i]:
            return False
    return True
def LoadOntology(file,ui):
    try:
        ontology = get_ontology(file).load()
        return ontology
    except Exception as err:
        ui.error(f"There was an error with {file} with error:{err}")

def SaveOntology(ontology,file,ui):
    try:
        if checkHttp(file)==True:
            ontology.save()
        else:
            ontology.save(file=file[7:])
    except Exception as err:
        ui.error(f"There was an error with {file} with error:{err}")
   
def findLabel(object):
    if object.label!=[]:
        label=object.label[0]
    else:
        label=str(object).split(".")[1]
    return label

def addData(ontology,data):
    for object in list(ontology.classes()):
        name=findLabel(object)
        keepParent=[]
        for parent in object.is_a:
            theParent=findLabel(parent)
            if theParent==name or theParent=="Thing":
                continue
            keepParent.append(theParent)
        data[0][name]=[object,name,keepParent,0,0]

    for relation in list(ontology.object_properties()):
        for range in list(relation.range):
            for domain in list(relation.domain):
                obj1=findLabel(domain)
                obj2=findLabel(range)
                name=findLabel(relation)

                data[0][obj1][3]=1
                data[0][obj2][3]=1
                if name not in data[1].keys():
                    data[1][name]=[relation,[obj1],name,obj2]
                else:
                    data[1][name][1].append(obj1)


def CreateObject(ontology,word,ui):
    try:
        with ontology:
            NewClass = types.new_class(word, (Thing,))
            NewClass.label = word
        return NewClass
    except Exception as err:
        ui.error(f"There was an error with {word} with error:{err}")
    

def ConnectObjects(ontology,connection,object1,object2,ui):
    try:
        with ontology:
            NewClass = types.new_class(connection,(object1 >> object2,))
        return NewClass
    except Exception as err:
        ui.error(f"There was an error with {connection}, {object1.label[0]} and {object2.label} with error:{err}")
    

def AddConnection(ontology,connection,object1,ui):
    try:
        with ontology:
            connection.domain.append(object1)
    except Exception as err:
        ui.error(f"There was an error with {connection} with error:{err}")

def Explanation(ontology,theClass,explanation,definedBy,ui):
    try:
        with ontology:
            class description(AnnotationProperty):
                pass
            if explanation!="":
                theClass.description.append(explanation)
            theClass.isDefinedBy = [definedBy]
    except Exception as err:
        ui.error(f"There was an error with {theClass.label[0]} with error:{err}")

def addParent(ontology,theClass,parent,ui):
    try:
        with ontology:
            if len(theClass.is_a)==1 and str(theClass.is_a[0]).split(".")[1]=="Thing":
                theClass.is_a=[parent]
            else:
                theClass.is_a.append(parent)
    except Exception as err:
        ui.error(f"There was an error with {theClass.label[0]} and {parent.label[0]} with error:{err}")