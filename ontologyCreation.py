from owlready2 import *
import types

def LoadOntology(file):
    ontology = get_ontology(file).load()
    return ontology

def SaveOntology(ontology):
    ontology.save()

def CreateObject(ontology,the_Class,parent):
    with ontology:
        if parent == None:
            NewClass = types.new_class(the_Class, (Thing,))
        else:
            NewClass = types.new_class(the_Class, (parent,))
    return NewClass

def ConnectObjects(ontology,connection,object1,object2):
    with ontology:
        NewClass = types.new_class(connection,(object1 >> object2,))
    return NewClass

def Explaination(ontology,the_Class,explaination,defined_by):
    with ontology:
        the_Class.comment.append(explaination)
        if defined_by==None:
            defined_by="You"
        the_Class.isDefinedBy = [defined_by]
