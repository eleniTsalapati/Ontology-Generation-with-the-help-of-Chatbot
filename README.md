# Chatbot-for-Ontology-Generation

## Summary of the Project
The perpose of this project is to use a ChatBot to create a new ontology by either using allready existing classes from outside ontologies or new of your own and to link them with respect of OntoClean rules and inheritance rules.

## How to use
After installing everyting (check how to download down bellow) you just run `python3 main.py` and a UI will apprear. You will have to use the UI. The UI will ask questions and you will have to answer either by yes or no (with clicking the button) or to write an answer. To search the ontology file you can use the button to find it faster.

***IMPORTANT: When writing a text be cearful with the grammar and syntax.***

For example the program will understand: *a cat eats the fish* or *cats eat fishes* but will **NOT** understand *cat eat fish*.

## Implementation of this repository :
### Hardware requirements: 
OS : Windows (Used for process), MscOS, Linux (any OS in this would work) Minimum RAM : 4GB Minimum Storage : As the NTLK data Set is not big a minimum of 100MB - 500MB should be suitable.

### Software requirements: 
For running the python files it is used Visual Studio Code. Any suitable IDE that can run python files, should also be suitable. (Python 3.9.6)

Also, if you want to connect your ontology with outside ontologies, you need a connection with a network so you can access the EMBL-EBI site that gives more information about each ontology through their API.

Also some libraries where used:
- Owalready2

  The Library "Owlready2" is used for the ontology creation-managment.

- NLTK 

  The Library "NLTK" is used for understanding the natural language.

- Requests

  The Library "Requests" is used for using outside ontologies. 

- Tkinter

  The Library "Tkinter" is used for the UI.

To download every Library together in Linux Environment use the following commands:
The python file *ntlk_data.py* will download the nessesary data set from NLTK.

```
pip3 install --upgrade pip
pip3 install --upgrade nltk
python3 ./commands/nltk_data.py
pip3 install owlready2
pip3 install requests
sudo apt-get install python-tk
```

To unistall in linux it is an easy task. Just use the following commands:

```
pip3 uninstall nltk
pip3 uninstall owlready2
pip3 uninstall requests
sudo apt-get remove python-tk
```

The above commands do not remove the NTLK data set. To remove the data set use the following commands: 
```
python3 ./commands/path_ntlk.py
rm -r OutputPath
``` 
