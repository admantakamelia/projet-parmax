import threading
import time
import random
import matplotlib.pyplot as plt
import networkx as nx

class Task:
    name = ""
    reads = [] #ce sont les variable que cette tache va lire
    writes = [] #ce sont les variable que cette tache va ecrire
    run = None #c'est une methode


class TaskSystem:
    tasksList = [] # tasksList est un tableau de taches de classe Task. Par defaut, il vaut le tableau vide.
    precedenceDict = {} # precedenceDist est la liste des precedences pour chacune des taches de taksList. Par defaut elle vaut la liste vide.
    taskNameDict = {} # taskNameDict est la liste des taches de classe Task, repertoriee par nom de tache. Par defaut elle vaut la liste vide.
    parMaxDict = {} # parMaxDict est la liste de dependances pour chacun des noms de taches. Par defaut, elle vaut la liste vide
    def __init__(self,tasksList,precedenceDict):
        # Initialisation de l'instance de classe TaskSystem
        self.tasksList = tasksList 
        self.precedenceDict = precedenceDict 
        #print("*** INIT de l'instance de TaskSystem")
        #print("    TasksList=[")
        for i in range(len(tasksList)):
            print("       "+tasksList[i].name)
        for task in tasksList: 
            self.taskNameDict[task.name] = task # On affecte la tache task a l'element d'index repere par le nom de la tache task.name de la liste taskNameDict 
            #print("       Tache "+task.name+': depend des taches '+str(self.getDependencies(task.name)))
            self.parMaxDict[task.name] = self.getDependencies(task.name) #  on affecte la liste minimuum de taches , dont la tache de nom task.name est dependante

       # print("     parMaxDict = " + str(self.parMaxDict))
        #print("*** FIN INIT de l'instance de TaskSystem")
    
    
    
 #on veut avoir les dépendences
# on va filtrer les dependences réelle
    def getDependencies(self,nomTache):
        # Retourne le tableau minimum des noms de taches dont 'nomtache' depend, en utilisant la regle de Bernstein. Si aucune, retourne []
        dependencies =  self.precedenceDict.get(nomTache).copy() # Liste des nom de tasks dependantes de la task de nom 'nomTache' donnee dans precedenceDict
        #print("++++ DEPENDANCES DE LA TACHE " + str(nomTache) + "=>" + str(dependencies))
        readsValues = self.getTaskByName((nomTache)).reads # readvalues prend la valeur lu .reads de la tache de classe Task pointee par le nom 'nomTache' dans la liste taskNameDict 
        #print("     set(readValues)="+str(set(readsValues)))
        for i in range(len(dependencies)): # Pour toutes les tasks dont nomTache depend
           # print("i="+str(i)+": set(readsValues)="+str(set(readsValues))+", self.getTaskByName(dependencies[i]).writes="+str(self.getTaskByName(dependencies[i]).writes))
            if len(list(set(readsValues).intersection(self.getTaskByName(dependencies[i]).writes))) ==0: # Application de la regle de Bernstein
                dependencies.pop(i)
                #si y a pas d intersection(len=0) donc ya pas réellement une dépendance, donc on enleve la dépendence 
                #exp pour T2 :il lit rien et la dependence T1 écris "X" =>intersiction=0 donc on supprime la dependence T1
        #print("     ==> Minimum dependencies (regle de Bernstein) ="+str(dependencies))
        #print("-- FIN getDepencies")
        return dependencies.copy()

    def getMaxParTaskSystem(self): #on affecte la liste minimum de taches(dependences reelles )après avoir utilisé la methodes getdependecies , dont la tache  est dependante
        s = TaskSystem(self.tasksList,self.parMaxDict)
        return s

    def runSeq(self):
        executedTasks = []
        for task in self.tasksList:
            self.recursiveSequenceRunner(executedTasks,task)


    def run(self):
        self.recurssiveParRunner(self.tasksList,self.parMaxDict,self.runparallel)



    def runparallel(self,tasksList):
    # Execution des threads associees aux taches task de classe Task de la lise de taches tasksList, dans l'odre des taches donne par tasksList
    # la fonction se termine lorsque la derniere tache est achevee
        threads = [] # tableau des threads associes aux taches de tasksList

        for task in tasksList:
        # je cree un thread par tache task de la liste tasksList et je le demarre
            t = threading.Thread(target=task.run)
            threads += [t]
            t.start()
        for t in threads:
            t.join() # je bloque la fin de runparallel tant que la tache associee au thread t n'est pas terminee

    #def runparallelDet(self,tasksList):
    # Execution des threads associees aux taches task de classe Task de la liste de taches tasksList, dans un ordre aleatoire
        #threads = []
        #n = len(tasksList)
        #random_list = random.sample(range(n), n)
        #for i in  range(len(random_list)):
            #t = threading.Thread(target=tasksList[i].run)
            #threads += [t]
            #t.start()
        #for t in threads:
            #t.join()





    def draw(self):
        # Construction du graphe de dependance des taches
        edges = []
        for key in self.precedenceDict.keys():

            if self.getDependencies(key):
                for value in self.getDependencies(key):
                    print(value)
                    edges += [(value,key)]

        G = nx.DiGraph()
        # chaque edge est de la forme (sommet1, sommet2, {'weight': weight})
        G.add_edges_from(edges)#chaque edge sera ajouté au graphe
        pos = nx.spectral_layout(G)  # positions de tous les sommets a l aide des vecteurs du graphe

        nx.draw(G, pos, with_labels=True, edge_color='b', arrowsize=20, arrowstyle='-|>', node_size=4000,
                node_color='g', font_size=16, font_color='w')
        plt.show()

    #comparer le temps de run et runSeq
    def parCost(self):
    # Durees comparees de 100 executions de taches en mode sequentiel, et en mode parallele
        totalTimeCostSeq = 0
        totalTimeCostPar = 0
        #compter le temps d'exécution de  runSeq
        for i in range(100):
            start = time.time()
            self.runSeq()
            end = time.time()

            totalTimeCostSeq += end - start

        timeCostSeq = totalTimeCostSeq/100

        # compter le temps d'exécution de  run
        for i in range(100):
            start = time.time()
            self.run()
            end = time.time()
            totalTimeCostPar += end - start

        timeCostPar = totalTimeCostPar/100

        print("time cost of runSeq: ",timeCostSeq)
        print("time cost of run: ",timeCostPar)


    def detTestRnd(self):
        pass




    def getTaskByName(self,taskName):
        # retourne la tache de classe Task dont le nom est 'taskName'
        return self.taskNameDict.get(taskName)

    def recursiveSequenceRunner(self,executedTasks,task):
    # Execution sequentielle de la tache task de classe Task, et de ses dependences, en executant en premier les taches non dependantes, puis les taches dependantes suivant le dictionnaire de taches utilise par la fonction getDependencies()
    # executedTasks est le tableau des taches  deja executees
    # task est la tache courante de classe Task, a executer apres avoir executer ses dependances eventuelles
        if len(self.getDependencies((task.name))) == 0 and task.name not in executedTasks:
        # Si la tache task de classe Task n'a pas encore ete executee (pas dans executedTasks) et qu'elle ne possede pas de dependance (self.getDependencie((task.name)) vaut le tableau vide []),
        # Alors
        #   La tache task de classe Task est executee
        #   On ajoute le nom de la tache task dans le tableau des noms de taches deja executees
            executedTasks += [task.name]
            task.run()

        else:
        # Sinon
        #   On appelle recursivement recursiveSequenceRunner() avec les taches dont depend la tache task, dont les noms sont le resultat de getDependencies
            for subTaskName in self.getDependencies(task.name):
                subTask = self.getTaskByName(subTaskName)
                self.recursiveSequenceRunner(executedTasks,subTask)
        #   Si la tache task n'a pas ete executee (pas dans le tableau executedTasks), je rajoute son nom dans executedTaks et j'execute la tache
            if task.name not in executedTasks:
                executedTasks += [task.name]
                task.run()

    def recurssiveParRunner(self,tasksList,depDict,runner):
    # Que fait la fonction?
    # tasksList est un tableau de taches task de classe Task
    # depDict est liste des dependances pour chacun des noms de taches
    # runner est la fonction donnnant l'ensembles des taches a executer en parallele
        parTasks = [] # Tableau des taches pouvant etre executee en parallele
        otherTasks = [] # Tableau des taches possedant une dependance selon le dictionnaire des dependance depDict
        otherTasksDepDict = {} # dictionnaire de dependances pour chacun des noms de taches du tableau otherTasks
       
        #renvoi les taches qui peuvent s'exécuetr en parallele
        for task in tasksList: # Pour toute tache de classe Task de la liste tasksList
            if len(depDict.get(task.name)) == 0: # Si aucune dependance trouvee
                parTasks += [task] # je l'ajoute au tableau de taches pouvant etre executees en parallele
            else: # Sinon
                otherTasks += [task] # je rajoute la tache task au tableau otherTasks
                otherTasksDepDict[task.name] = depDict.get(task.name).copy() # et je mets a jour la liste otherTasksDepDict, suivant l'index donne par le nom de la tache task, avec la valeur 

        
        #j'enleve les taches dependentes qui peuvent s'exécuter en parallele
        for task in otherTasks: # pour toutes les taches task dont une dependance a priori
            for subTaskName in depDict.get(task.name):
                if self.getTaskByName(subTaskName) in parTasks: # si la dependance est une tache pouvant etre exetutee en parallele,
                    otherTasksDepDict.get(task.name).remove(subTaskName) # alors, je retire cette tache, qui a deja ete executee recursivement par un runner(parTasks)
        
        runner(parTasks) # Execution des taches pouvant etre executees en parallele 
        if otherTasksDepDict:
            self.recurssiveParRunner(otherTasks,otherTasksDepDict,self.runparallel)
            #otherTask =somme
            #otherTasksDepDict c est un dictionnaire {somme[]}
        else:
            return


