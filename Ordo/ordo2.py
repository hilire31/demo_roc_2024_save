from ortools.sat.python import cp_model

# Paramètres d'exemple
animaux = ['a1', 'a2', 'a3','a4']
bateaux = ['b1', 'b2',]
temps_traversee = {('a1', 'b1'): 2, ('a1', 'b2'): 2, 
                   ('a2', 'b1'): 2, ('a2', 'b2'): 2, 
                   ('a3', 'b1'): 3, ('a3', 'b2'): 3,
                   ('a4', 'b1'): 3, ('a4', 'b2'): 3}
due_dates = {'a1': 20, 'a2': 20, 'a3': 20,'a4':20}
capacite_bateaux = {'b1': 2, 'b2': 1}

# Créer le modèle
model = cp_model.CpModel()

# Variables de décision
x = {}
for i in animaux:
    for j in bateaux:
        x[(i, j)] = model.NewBoolVar(f'x_{i}_{j}')

S = {}
for i in animaux:
    S[(i,j)] = model.NewIntVar(0, max(due_dates.values()), f'S_{i}_{j}')

# Makespan
makespan = model.NewIntVar(0, max(due_dates.values()) + max(temps_traversee.values()), 'makespan')
# Contraintes : chaque animal doit être assigné à un bateau

for i in animaux:
    model.Add(sum(x[(i, j)] for j in bateaux) == 1)

# Contraintes : capacité des bateaux
for j in bateaux:
    model.Add(max_occ([S[(i, j)] for i in animaux]) <=capacite_bateaux[j])
    model.Add(sum(x[(i, j)] for i in animaux) <= capacite_bateaux[j])

# Contraintes : respect des due-dates et calcul du makespan
for i in animaux:
    for j in bateaux:
        model.Add(S[i] + temps_traversee[(i, j)] * x[(i, j)] <= due_dates[i])
        model.Add(makespan >= S[i] + temps_traversee[(i, j)] * x[(i, j)])

# Fonction objectif : minimiser le makespan
model.Minimize(makespan)

# Résolution du modèle
solver = cp_model.CpSolver()
status = solver.Solve(model)

# Afficher les résultats
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(f"Statut : {solver.StatusName(status)}")
    for i in animaux:
        for j in bateaux:
            if solver.BooleanValue(x[(i, j)]):
                print(f"L'animal {i} traverse sur le bateau {j} et commence à {solver.Value(S[i])}")
    print(f"Makespan : {solver.Value(makespan)}")
else:
    print("Aucune solution trouvée.")
