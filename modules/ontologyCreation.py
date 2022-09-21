from owlready2 import *

def LoadOntology(file):
    ontology = get_ontology(file).load()
    return ontology

def SaveOntology(ontology):
    ontology.save()

def CreateObject(ontology,word,parent):
    with ontology:
        if parent == None:
            NewClass = types.new_class(word, (Thing,))
        else:
            NewClass = types.new_class(word, (parent,))
    return NewClass

def addData(ontology,classes):
    for object in list(ontology.classes()):
        name=str(object).split(".")[1]
        parent=str(list(object.ancestors())[0]).split(".")[1]
        if parent==name:
            parent="None"
        print(name,parent)
        classes[0][name]=[object,name,parent,0,0]

    for relation in list(ontology.object_properties()):
        for domain in list(relation.domain):
            for range in list(relation.range):
                name=str(relation).split(".")[1]
                obj1=str(domain).split(".")[1]
                obj2=str(range).split(".")[1]
                classes[0][obj1][4]=1
                classes[0][obj2][4]=1
                classes[1][name]=[relation,obj1,name,obj2]


def ConnectObjects(ontology,connection,object1,object2):
    with ontology:
        NewClass = types.new_class(connection,(object1 >> object2,))
    return NewClass

def Explanation(ontology,theClass,explanation,definedBy):
    with ontology:
        class description(AnnotationProperty):
            pass
        theClass.description.append(explanation)
        theClass.isDefinedBy = [definedBy]

def changeParent(ontology,subject,parent):
    with ontology: 
        subject.is_a=[parent]