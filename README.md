# projet de parallélisation maximale

Le projet est constitué d’un fichier contenant une classe Task et une classe TaskSystem, nommé Task.py, et d’un fichier de test test.py, tous deux écrits en Python.

## Pour que le programme fonctionne faut l’installation de deux librairies :
	Matplotlib 
**Pip install matplotlib**
	
 Networkx
 
**Pip install networkx option**


Une tâche abstraite, issue de la classe Task, est définie par un nom (chaîne de caractères), nommé ‘name’, une fonction d’exécution Python, nommée ‘run’, un tableau de préconditions (chaines de caractères), nommé ‘reads’ définissant l’ensembles des variables dont les valeurs doivent être connues avant d’exécuter la fonction ‘run’, et un tableau de postcondition (chaines de caractères), nommé ‘writes’, définissant l’ensemble des variables résultats de la fonction ‘run’.
 La classe TaskSystem défini un tableau de tâches ‘tasksList’ de classe Task à exécuter, avec un dictionnaire d’ordonnancement de tâches ‘precedenceDict’, qui est un tableau dont les éléments sont repérés par un nom de tâches et la valeur est un tableau de noms de tâches devant être exécutées préalablement à l’exécution de la tâche.
 ## Trois fonctions importante dans le projet
 
  ### fonction getDependencies()
La fonction de TaskSystem gérant le lien entre une tâche de nom ‘nomTache’ et d’autres tâches de ‘taskList’ est getDependencies(nomTache), qui retourne le tableau minimum des noms de tâches dont 'nomTache' dépend, en utilisant la règle de Bernstein. 
Cette fonction prend en compte à la fois les données de precedenceDict et les pré et post conditions associées aux tâches de taskList.

  ### fonction runSeq()
La foncion runSeq() permet l’exécution séquentielle des tâches de taskList. Elle utilise récursivement la fonction recursiveSequenceRunner(executedTasks,task), executedTasks étant le tableau de tâches de classe Task déjà exécutées et task la tâche de classe Task à exécuter. Dans ce cadre, une tâche est exécutée si l’appel à getDependencies(task) ne retourne aucune dépendance (tableau vide).

 ### fonction run()
La fonction run() permet l’exécution en parallèle, si possible, des tâches de taskList, en utilisant la librairies threading. Elle utilise récursivement la fonction recurssiveParRunner(self,tasksList,depDict,runner), tasksList étant la liste des tâches à exécuter de classe Task, depDict étant le dictionnaire de dépendance des tâches et runner étant la fonction à exécuter. Cette fonction va extraire et exécuter en parallèle sous des threads des tâches qui ne possèdent aucune dépendance.

La fonction Draw() affiche graphiquement le graphe de dépendance des tâches.
La fonction parCost() calcule le temps d’exécution de l’ensemble des tâches de taskList par la méthode séquentielle runSeq() et la méthode parallèle utilisant des thread run().

Le fichier test.py crée un exemple très simple, avec trois tâches T1, T2 et somme, dépendant de T1 et T2.


<img width="476" alt="parmax" src="https://user-images.githubusercontent.com/130518502/232606497-7d7a049e-0b3a-455b-9b41-cad72cf66216.png">


