import math

def calcul_distance(x,y):
    result = 0

    for i in range(len(x[0])) :
        result+=(y[0][i] - x[0][i])**2
    return math.sqrt(result)

def calcul_distance_total(tab,mon_image):
    result = []
    for x in tab:
        result.append((calcul_distance(x,mon_image),x[1]))
    result.sort()
    return result

def find(distances, k=3):
    k_voisins = distances[:k]
    
    votes = {}
    
    for distance, nom_image in k_voisins:
        vrai_chiffre = str(nom_image)[0] 
        
        if vrai_chiffre in votes:
            votes[vrai_chiffre] += 1
        else:
            votes[vrai_chiffre] = 1
            
    print(f"Détail des {k} votes : {votes}")
            
    meilleur_chiffre = None
    max_votes = 0
    
    for chiffre, nb_votes in votes.items():
        if nb_votes > max_votes:
            max_votes = nb_votes
            meilleur_chiffre = chiffre
            
    return meilleur_chiffre


def main():
    # test1 = ([0.4072751322751323, 0.36797661578434554, 0.37512179278986685, 0.3049691458265671, 0.3835660928873011, 0.4, 0.6], '9ss.png')
    # test2 = ([0.2898962863834058, 0.36006924408540103, 0.3808424697057126, 0.29486439699942296, 0.36295441431044434, 0.4, 0.6], '9t.png')
    # test3 = ([0.30905832518735743, 0.2878228782287823, 0.33210332103321033, 0.34211913547706907, 0.29836584080126516, 0.4, 0.4], '0t.png')
    # test4 = ([0.4132796780684105, 0.3784485556637455, 0.3073677377474846, 0.38396624472573837, 0.37877312560856863, 0.4, 0.6], '6ss.png')
    # print(calcul_distance(test1,test4))
    ...

if __name__ == "__main__":
    main()