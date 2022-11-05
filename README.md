# Chatbot for Ontology Generation

## Summary of the Project
The purpose of this project is to use a ChatBot to create a new ontology by either taking already existing classes from external ontologies or creating new classes and linking them according to OntoClean rules and inheritance rules.

## How to use
After installing everything (check how to download it below), you just run `python3 main.py` and a UI will appear. The user will have to use the UI. The UI will ask questions and the user will have to answer either by clicking the buttons or writing the response. To search the ontology file, the user can use the button to find it faster.

***IMPORTANT: When writing a text, be careful with the grammar and syntax.***

For example, the program will understand: *a cat eats the fish* or *cats eat fishes* but will **NOT** understand *cat eat fish*.

***Also for numerous Continuous nouns you have to connect them with the underscore "_".***

## Requirements: 
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

## How to install Python
### Windows
You can install python for Windows in the link: https://www.python.org/downloads/windows/ 

I would suggest clicking the PATH option otherwise the libraries might not download correcrty.

### Linux
You can install python for Linux in the link: https://www.python.org/downloads/source/
or by running in the following commands:
```
sudo apt-get update
sudo apt-get install python3.9
```

## Install Libraries without anaconda:
**If you have not accapted the Path Option on Windows then you have to be cearfull downloading the libraries.**

First you have to  open a command prompt on Windows or a terminal in Linux in the folder of the repository.
If the path of the command prompt or terminal is not correct, then use `cd path_of_the_folder` to go to the correct folder.

To download every Library together, use the following commands:

```
pip install --upgrade pip
pip install --upgrade nltk
pip install owlready2
pip install requests
pip install tk
```

It is neccasary to dowload the data set from NLTK. You can do it with the following command:
```
python ./commands/nltk_data.py
```

## Install Libraries with anaconda:
First you have to dowload the chatBot_ontology_creation_env.yaml and open anaconda prompt. 
Then run in the prompt the following command to create the enviroment with the installed libraries:
```
conda env create -f path\chatBot_ontology_creation_env.yaml
```

Then you have to activate the enviroment by typing `conda activate chatBot_ontology_creation_env`.

Then you have to cd to the github file (Chatbot-for-Ontology-Generation) that you have downloaded by `cd path\folder`.

It is neccasary to dowload the data set from NLTK. You can do it with the following command:
```
python ./commands/nltk_data.py
```

You are ready to run `python main.py`.

## Uninstall Libraries without anaconda:
First you have to use the open a command prompt on Windows or in a terminal in Linux in the folder of the repository.
If the path is not correct then use `cd path_of_the_folder` to go to the correct folder.

To uninstall the NTLK data set use the following command to find the file: 
```
python ./commands/path_nltk.py
``` 
and either find the folder and delete it 

Or only in **Linux terminal** use the following command:
```
rm -r OutputPath
``` 
where the OutputPath is the result of the previous command.

To uninstall the Libraries just use the following commands:
```
pip uninstall nltk
pip uninstall owlready2
pip uninstall requests
pip uninstall tk
```

## Uninstall Libraries with anaconda:

First, to uninstall the NTLK data set use the following command to find the file: 
```
python ./commands/path_nltk.py
``` 
and find the folder and delete it. 

If the enviroment is still activated, then you have to deactivate it: `conda deactivate`.
Then you find the folder that holds the enviroment (usually under c:/users/[user_name]/anacoda[number]/env) and delete that folder and you are done.
