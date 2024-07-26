import pulp

# Paramètres d'exemple
animaux = ['a1', 'a2', 'a3']
bateaux = ['b1', 'b2']
temps_traversee = {('a1', 'b1'): 2, ('a1', 'b2'): 2, 
                   ('a2', 'b1'): 2, ('a2', 'b2'): 2, 
                   ('a3', 'b1'): 3, ('a3', 'b2'): 3}
due_dates = {'a1': 5, 'a2': 4, 'a3': 6}
capacite_bateaux = {'b1': 2, 'b2': 1}

# Modèle
model = pulp.LpProblem("Ordonnancement", pulp.LpMinimize)

# Variables de décision
x = pulp.LpVariable.dicts("x", [(i,j) for i in animaux for j in bateaux], cat='Binary')
S = pulp.LpVariable.dicts("S", animaux, lowBound=0, cat='Continuous')

# Fonction objectif : minimiser le retard total
retard_total = pulp.lpSum([pulp.lpMax([0, S[i] + temps_traversee[(i, j)] - due_dates[i]]) * x[(i, j)] 
                           for i in animaux for j in bateaux])
model += retard_total

# Contraintes
# Chaque animal doit être assigné à un bateau
for i in animaux:
    model += pulp.lpSum([x[(i, j)] for j in bateaux]) == 1

# Capacité des bateaux
for j in bateaux:
    model += pulp.lpSum([x[(i, j)] for i in animaux]) <= capacite_bateaux[j]

# Respect des due-dates
for i in animaux:
    for j in bateaux:
        model += S[i] + temps_traversee[(i, j)] * x[(i, j)] <= due_dates[i]

# Résolution du modèle
model.solve()

# Résultats
print("Statut:", pulp.LpStatus[model.status])
for i in animaux:
    for j in bateaux:
        if pulp.value(x[(i, j)]) == 1:
            print(f"L'animal {i} traverse sur le bateau {j} et commence à {pulp.value(S[i])}")

# Afficher le retard total
print("Retard total:", pulp.value(retard_total))
