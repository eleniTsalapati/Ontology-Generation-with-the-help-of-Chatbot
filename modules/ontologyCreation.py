from owlready2 import *
import types

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
