from re import sub
import modules.chatbotTalks as talk
import modules.ontologyCreation as creation
import modules.chatbotHears as hear
import modules.searchOntology as search
import modules.utility as utility

def checkInheritanceAndChange(ontology,word,parent,theClass,ui):
    answer=utility.question_arg2_with_yes_or_No(ui,talk.ontoCheck,parent,word)
    if answer==1:
        theClass[0][word][3]=parent
        creation.changeParent(ontology,theClass[0][word][0],theClass[0][parent][0])
        ui.changeParent(word,parent)
    else:
        answer=utility.question_arg2_with_yes_or_No(ui,talk.identityComponentOf,parent,word)
        if answer==1:
            # mark as used
            theClass[0][parent][4]=1
            theClass[0][word][4]=1
            # create relation
            relation="componentOf"+word.title()
            theClass[1][relation]=[creation.ConnectObjects(ontology,relation,theClass[0][parent][0],theClass[0][word][0]),parent,relation,word]  
        else:
            ui.rememberOneTime("Ok now something new.\n")
            answer=utility.question_arg2_with_yes_or_No(ui,talk.identityComponentOf,word,parent)
            if answer==1:
                # mark as used
                theClass[0][parent][4]=1
                theClass[0][word][4]=1
                # create relation
                relation="componentOf"+parent.title()
                theClass[1][relation]=[creation.ConnectObjects(ontology,relation,theClass[0][word][0],theClass[0][parent][0]),word,relation,parent]       
            else:
                # check UNITY
                answer=utility.question_arg2_with_yes_or_No(ui,talk.unityComposedOf,parent,word)
                if answer==1:
                    # mark as used
                    theClass[0][parent][4]=1
                    theClass[0][word][4]=1
                    # create relation
                    relation="composedOf"+word.title()
                    theClass[1][relation]=[creation.ConnectObjects(ontology,relation,theClass[0][parent][0],theClass[0][word][0]),parent,relation,word]       
                else:
                    ui.rememberOneTime("Ok now something new.\n")
                    answer=utility.question_arg2_with_yes_or_No(ui,talk.unityComposedOf,word,parent)
                    if answer==1:
                        # mark as used
                        theClass[0][parent][4]=1
                        theClass[0][word][4]=1
                        # create relation
                        relation="composedOf"+parent.title()
                        theClass[1][relation]=[creation.ConnectObjects(ontology,relation,theClass[0][word][0],theClass[0][parent][0]),word,relation,parent]
                    else:    
                        ui.rememberOneTime("I cannot understand how the connection goes so I will not use this connection.\n")
                        ui.rememberOneTime("Please fix the connection between \""+parent+"\" - \""+word+"\"")

def checkInheritanceAndCreate(ontology,word,parent,theClass,ui):
    # check if there is a parent to check for the inheritance
    if parent!=None:
        # check if the inheritance is correct
        answer=utility.question_arg2_with_yes_or_No(ui,talk.ontoCheck,parent,word)
    else:
        answer=1
    
    # there is a parent and there is wrong with the inheritance
    if answer==-1:
        # create the word
        theClass[0][word]=[creation.CreateObject(ontology,word,None),word,"None",0,0]
        
        # check IDENTITY
        answer=utility.question_arg2_with_yes_or_No(ui,talk.identityComponentOf,parent,word)
        if answer==1:
            # mark as used
            theClass[0][parent][4]=1
            theClass[0][word][4]=1
            # create relation
            relation="componentOf"+word.title()
            theClass[1][relation]=[creation.ConnectObjects(ontology,relation,theClass[0][parent][0],theClass[0][word][0]),parent,relation,word]  
        else:
            ui.rememberOneTime("Ok now something new.\n")
            answer=utility.question_arg2_with_yes_or_No(ui,talk.identityComponentOf,word,parent)
            if answer==1:
                # mark as used
                theClass[0][parent][4]=1
                theClass[0][word][4]=1
                # create relation
                relation="componentOf"+parent.title()
                theClass[1][relation]=[creation.ConnectObjects(ontology,relation,theClass[0][word][0],theClass[0][parent][0]),word,relation,parent]       
            else:
                # check UNITY
                answer=utility.question_arg2_with_yes_or_No(ui,talk.unityComposedOf,parent,word)
                if answer==1:
                    # mark as used
                    theClass[0][parent][4]=1
                    theClass[0][word][4]=1
                    # create relation
                    relation="composedOf"+word.title()
                    theClass[1][relation]=[creation.ConnectObjects(ontology,relation,theClass[0][parent][0],theClass[0][word][0]),parent,relation,word]       
                else:
                    ui.rememberOneTime("Ok now something new.\n")
                    answer=utility.question_arg2_with_yes_or_No(ui,talk.unityComposedOf,word,parent)
                    if answer==1:
                        # mark as used
                        theClass[0][parent][4]=1
                        theClass[0][word][4]=1
                        # create relation
                        relation="composedOf"+parent.title()
                        theClass[1][relation]=[creation.ConnectObjects(ontology,relation,theClass[0][word][0],theClass[0][parent][0]),word,relation,parent]
                    else:    
                        ui.rememberOneTime("I cannot understand how the connection goes so I will not use this connection.\n")
                        ui.rememberOneTime("Please fix the connection between \""+parent+"\" - \""+word+"\"")
        return "None"
    else:
        if parent==None:
            # there was no parent 
            theClass[0][word]=[creation.CreateObject(ontology,word,parent),word,"None",0,0]
            return "None"
        else:
            # the parent was correct
            theClass[0][word]=[creation.CreateObject(ontology,word,theClass[0][parent][0]),word,parent,0,0]
            return parent

def find_definition_of_Noun(noun,parent,classes,ui):
    kids=None
    definition=None

    if noun in classes[0].keys() and classes[0][noun][3]==1:
            answer=-1
    else:
        answer= utility.question_arg1_with_yes_or_No(ui,talk.FindDefinition,noun)
        
    # The user wants to find the definition
    if answer==1:
        try:
            # search the definition
            (definition,definedBy,kids)=search.searchForTerm(noun,parent,ui)
        except:
            ui.rememberOneTime("There is an error with the code either because there is a bug or you do not have access to Internet\n")

    # if the search definition was not selected
    if  definition==None:

        # ask if the user want to give definition
        answer= utility.question_arg1_with_yes_or_No(ui,talk.AskDefinition,noun)

        # The user wants to give the definition
        if answer == 1:
            ui.changeMessage(talk.YourDefinition(noun))
            answerUI=ui.hear()
            definition=hear.GetDefinition(answerUI)
            definedBy="You"
        # The user wants to do something else
        else:
            # See if the user wants to keep without definition
            answer= utility.question_arg1_with_yes_or_No(ui,talk.KeepWord,noun)
            
            # The user wants to keep without definition
            if answer==1:
                definition=""
                definedBy=""
            # The user does not want to keep the word
            else:
                definition=None
                definedBy=None

    return (definition,definedBy,kids)

def what_the_ontology_should_answer(ontology,classes,ui):

    previousNouns=classes[0].keys()
    previousRelated=classes[1].keys()

    # See what the ontology should answer
    ui.changeMessage(talk.WhatOntologyToAnswer())
    answerUI=ui.hear()
    (nouns,relationships)=hear.WhatOntologyToAnswer(answerUI,ui)

    # For all the nouns that we have
    for noun in nouns.keys():
        parent=nouns[noun]

        # we have already seen this noun in a previous question
        if noun in previousNouns:
            continue
        
        # find the definition of the noun
        (definition,definedBy,kids)=find_definition_of_Noun(noun,parent,classes,ui)

        # if the user do not want to keep the noun 
        if  definition==None:
            continue
        
        # Create into the ontology the word
        checkInheritanceAndCreate(ontology,noun,parent,classes,ui)
        # and give the definition
        creation.Explanation(ontology,classes[0][noun][0],definition,definedBy)
            

        # check if there were any kids
        if kids !=None:
            # for all the kids
            for (kid,definition,definedBy) in kids:
                # Create the kid 
                classes[0][kid]=[creation.CreateObject(ontology,kid,classes[0][noun][0]),kid,noun,1,0]
                # add the definition
                if definition!="":
                    creation.Explanation(ontology,classes[0][kid][0],definition,definedBy)

    # for all relationships
    keptNouns=classes[0].keys()
    for relation in relationships.keys():
        # we have already seen this relation in a previous question
        if relation in previousRelated:
            continue

        # if one object is not created then do not create the relationship
        obj1=relationships[relation][0]
        obj2=relationships[relation][1]
        if obj1 not in keptNouns or obj2 not in keptNouns:
            continue

        # mark as used
        classes[0][obj1][4]=1
        classes[0][obj2][4]=1
        # create the relationship
        classes[1][relation]=[creation.ConnectObjects(ontology,relation,classes[0][obj1][0],classes[0][obj2][0]),obj1,relation,obj2]

def more_types(ontology,classes,seen,ui):
    
    nouns=list(classes[0].keys())
    for noun in nouns:

        # if the noun has already been seen 
        # do not ask for more types
        if noun in seen:
            ui.rememberOneTime("I have already asked for \""+noun+"\", so I will not ask again.")
            continue
        if classes[0][noun][3]==1:
            ui.rememberOneTime("The \""+noun+"\" is taken from the web so I will not ask for subcategories.")
            continue


        seen.append(noun)
        
        # ask if you want to get the different types
        ui.rememberTableOnce()
        answer= utility.question_arg1_with_yes_or_No(ui,talk.AskDifferentTypes,noun)
        if answer==1:

            # ask the types
            ui.rememberTableOnce()
            ui.changeMessage(talk.GetDifferentTypes(noun))
            answerUI=ui.hear()
            types=hear.GetTypes(answerUI,ui)

            # for each type from the different types 
            for type in types:
            
                (definition,definedBy,kids)=find_definition_of_Noun(type,noun,classes,ui)
            
                if  definition==None:
                    continue

                # Create into the ontology the word
                checkInheritanceAndCreate(ontology,type,noun,classes,ui)
                # and give the definition
                creation.Explanation(ontology,classes[0][type][0],definition,definedBy)
                    
                if kids !=None:
                    for (kid,definition,definedBy) in kids:
                        classes[0][kid]=[creation.CreateObject(ontology,kid,classes[0][noun][0]),kid,noun,1,0]
                        if definition!="":
                            creation.Explanation(ontology,classes[0][kid][0],definition,definedBy)

def hyperClass(ontology,classes,ui):
    # get the subject
    ui.rememberTableOnce()
    ui.changeMessage(talk.AskForHyper())
    answerUI=ui.hear()
    subjects=hear.WhatOntologyToAnswer(answerUI,ui)[0]

    for subject in subjects:

        parent=None
        # find parent
        ui.rememberTableOnce()
        answer=utility.question_arg1_with_yes_or_No(ui,talk.AskHyperOfHyper,subject)

        if answer==1:
            ui.rememberTableOnce()

            ui.changeMessage(talk.FindHyperOfHyper(subject))
            answerUI=ui.hear()
            parent=hear.FindNounInDataBase(answerUI,classes)
            if parent==None:
                ui.rememberOneTime("No word in the DataBase was found\n")
            parent=checkInheritanceAndCreate(ontology,subject,parent,classes,ui)
        else:
            classes[0][subject]=[creation.CreateObject(ontology,subject,None),subject,"None",0,0]

        (definition,definedBy,kids)=find_definition_of_Noun(subject,parent,classes,ui)

        # and give the definition
        creation.Explanation(ontology,classes[0][subject][0],definition,definedBy)

        # create kids from the search that we did 
        if kids !=None:
            for (kid,definition,definedBy) in kids:
                classes[0][kid]=[creation.CreateObject(ontology,kid,classes[0][subject][0]),kid,subject,1,0]
                if definition!="":
                    creation.Explanation(ontology,classes[0][kid][0],definition,definedBy)
        
        # find kids
        ui.rememberTableOnce()
        ui.changeMessage(talk.BecomeHyper(subject))
        answerUI=ui.hear()
        words=hear.FindNounsInDataBase(answerUI,classes,ui)

        for word in words:
            checkInheritanceAndChange(ontology,word,subject,classes,ui)
            # creation.changeParent(ontology,classes[0][word][0],classes[0][subject][0])
            # ui.changeParent(word,subject)
        ui.checkChange(classes)
    
