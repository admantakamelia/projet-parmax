from Task import *

X= None
Y= None
Z= None

def runT1():
    global X
    #print("executer la tache 1")
    X = 1

def runT2():
    global Y
    #print("executer la tache 2")
    Y = 2

def runTsomme():
    global X, Y, Z
    #print("executer la tache somme")
    Z = X + Y

t1 = Task()
# Dans la Task nommee "T1", je me prepare a affecter 1 a X (dans .writes) par l'intermediaire de la fonction runT1
t1.name = "T1"
t1.writes = ["X"]
t1.run = runT1

t2 = Task()

t2.name = "T2"
t2.writes= ["Y"]
t2.run = runT2

tsomme = Task()
tsomme.name = "somme"
tsomme.reads = ["X", "Y"]
tsomme.writes = ["Z"]
tsomme.run = runTsomme

t1.run() # j'execute la fonction d'affetation de "X" a 1
print(X) 
t2.run() 
print(Y) 

tsomme.run() 
print(Z) 



s1 = TaskSystem([t1,t2,tsomme],{"T1" : [], "T2": ["T1"], "somme": ["T1", "T2"]})
# J'initialise le TaskSystem s1 avec le tableau de trois Task [t1, t2, somme] et le dictionnaire de dependances des Tasks
 #liste de taches,le dictionnaire qui donne les contrainte de précédence
                                     #ces taches est ce que elles dependent d'autre taches avant de s'exécuter
#s1 doit etre un systeme de parallélisme maximale et ceci on realisont les taches

#print('Je vais lancer getDependencies T2')
#print(s1.getDependencies("T2"))

s1.runSeq()

print(X)
print(Y)
print(Z)

s1.run()

print(X)
print(Y)
print(Z)

s1.draw()

s1.parCost()


