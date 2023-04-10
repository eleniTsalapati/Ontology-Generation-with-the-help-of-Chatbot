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
def LoadOntology(file,errorFunction):
    try:
        ontology = get_ontology(file).load()
        return ontology
    except Exception as err:
        errorFunction(f"There was an error with {file} with error:{err}")
        return None

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

def addData(ontology,data,ui):
    for object in list(ontology.classes()):
        name=findLabel(object)
        keepParent=[]
        for parent in object.is_a:
            theParent=findLabel(parent)
            if theParent==name or theParent=="Thing":
                continue
            keepParent.append(theParent)
        data[0][name]=[object,name,keepParent,0,0]
        ui.AddToTableTerm(name)
    for relation in list(ontology.object_properties()):
        obj1=[]
        obj2=[]

        try:
            for domain in relation.domain[0].get_Classes():
                label=findLabel(domain)
                data[0][label][3]=1
                obj1.append(label)
        except:
            label=findLabel(relation.domain[0])
            data[0][label][3]=1
            obj1.append(label)
        key=findLabel(relation)

        try:
            for range in relation.range[0].get_Classes():
                label=findLabel(range)
                data[0][label][3]=1
                obj2.append(label)
        except:
            label=findLabel(relation.range[0])
            data[0][label][3]=1
            obj2.append(label)

        data[1][key]=[relation,obj1,key,obj2]
        ui.AddToTableRelationship(key)



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
    

def AddConnection(ontology,connection,object1,object2,ui):
    try:
        with ontology:
            try:
                if object1 not in connection.domain[0].get_Classes():
                    connection.domain= connection.domain[0] | object1
            except:
                if object1 not in connection.domain:
                    connection.domain= connection.domain[0] | object1
            try:
                if object2 not in connection.range[0].get_Classes():
                    connection.range= connection.range[0] | object2
            except:
                if object2 not in connection.range:
                    connection.range= connection.range[0] | object2
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

def RemoveDomain(ontology,relationship,domain,ui):
    try:
        with ontology:
            object=[]
            for i in relationship.domain[0].get_Classes():
                if i == domain:
                    continue
                object.append(i)
            for i,value in enumerate(object):
                if i ==0:
                    relationship.domain=value
                else:
                    relationship.domain= relationship.domain[0] | value
    except Exception as err:
        ui.error(f"There was an error with {relationship} with error:{err}")

def RemoveRange(ontology,relationship,range,ui):
    try:
        with ontology:
            object=[]
            for i in relationship.range[0].get_Classes():
                if i == range:
                    continue
                object.append(i)
            for i,value in enumerate(object):
                if i ==0:
                    relationship.range=value
                else:
                    relationship.range= relationship.range[0] | value
    except Exception as err:
        ui.error(f"There was an error with {relationship} with error:{err}")

