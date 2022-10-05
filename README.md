# Chatbot for Ontology Generation

## Summary of the Project
The purpose of this project is to use a ChatBot to create a new ontology by either taking already existing classes from external ontologies or creating new classes and linking them concerning OntoClean rules and inheritance rules.

## How to use
After installing everything (check how to download it below), you just run `python3 main.py` and a UI will appear. The user will have to use the UI. The UI will ask questions and the user will have to answer either by yes or no (by clicking the button) or write an answer. To search the ontology file, the user can use the button to find it faster.

***IMPORTANT: When writing a text, be careful with the grammar and syntax.***

For example, the program will understand: *a cat eats the fish* or *cats eat fishes* but will **NOT** understand *cat eat fish*.

## Implementation of this repository :
### Hardware requirements: 
OS : Windows, MscOS, Linux (any OS in this would work). Minimum RAM : 4GB. Minimum Storage : As the NTLK Data Set size is insignificant, a minimum of 1MB - 50MB should be suitable.

### Software requirements: 
Any suitable IDE that can run python files should also be suitable. (Python 3.9.6)

Also, suppose the user wants to connect the ontology with external ontologies. In that case, a network connection is needed to access the EMBL-EBI site that gives more information about each ontology through their API.

Also, the following libraries are used:
- Owalready2

  The Library "Owlready2" is used for the ontology creation-management.

- NLTK 

  The Library "NLTK" is used for understanding the natural language.

- Requests

  The Library "Requests" is used for API. 

- Tkinter

  The Library "Tkinter" is used for the UI.

### Install and Uninstall in Linux Environment:
To download every Library together in **Linux** Environment, use the following commands:
The python file *ntlk_data.py* will download the necessary data set from NLTK.

```
pip3 install --upgrade pip
pip3 install --upgrade nltk
python3 ./commands/nltk_data.py
pip3 install owlready2
pip3 install requests
sudo apt-get install python-tk
```

To uninstall in **Linux** is an easy task. Just use the following commands:

```
pip3 uninstall nltk
pip3 uninstall owlready2
pip3 uninstall requests
sudo apt-get remove python-tk
```

The above commands do not remove the NTLK data set. To remove the data set, use the following commands: 
```
python3 ./commands/path_ntlk.py
rm -r OutputPath
``` 
