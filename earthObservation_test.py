from owlready2 import *

onto = get_ontology("file:////media/akis/Ubuntu-Windows/Uni/Chatbot-for-Ontology-Generation/ontologies/earhObservation_test.owl").load()

with onto:
    # Q:What questions do you want your ontology to be able to answer
    # A:Enumerate all remote sensors from satellites ->
    #  remote sensors, satellites,from
    class Satellites(Thing):
        pass
    class RemoteSensors(Thing):
        pass
    class comeFrom(RemoteSensors>>Satellites):
        pass
    # Q:What is a remote sensor
    # A:Remote sensor is x
    # --------
    RemoteSensors.isDefinedBy = ["X"]

    # Q:are there different types of remote sensoers
    # A: yes
    # Q:Enumerate all different types of remote sensors
    # A: altimeter,optical sensor

    class Altimeter(RemoteSensors):
        pass

    class OpticalSensor(RemoteSensors):
        pass

    # Q:Radiometer seems a relevant class, is it a remote sensor?
    # A: yes

    class Radiometer(RemoteSensors):
        pass

onto.save()
