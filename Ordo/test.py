import tkinter as tk
def ordonnancement_taches(taches):
    # Simule un ordonnancement de tâches basé sur le debut (ex: plus tot d'abord)
    return sorted(taches, key=lambda x: x[2])

def afficher_resultat():
    # Récupérer le résultat de l'ordonnancement

    # Effacer le contenu du canvas actuel
    canvas.delete("all")
    cap=3
    

    # Paramètres de dessin
    x_depart = 50  # Position de départ horizontale
    y_depart = 100  # Position verticale fixe pour toutes les tâches
    hauteur = 40  # Hauteur des rectangles

    # Couleurs des tâches
    couleurs = ["#FF6347", "#4682B4", "#32CD32", "#FFD700", "#FF69B4"]
    ordo=ft(taches,cap)
    # Ajouter les rectangles colorés sur la même ligne

    for cren in ordo:
        for i in cren:
            (nom, duree, debut, fin, poids)=taches[i]
            couleur = couleurs[i % len(couleurs)]  # Choisir une couleur
            largeur = duree * 10  # Exemple: 10 pixels par minute
            hauteur = 40 * poids
            canvas.create_rectangle(x_depart, y_depart, x_depart + largeur, y_depart + hauteur, fill=couleur)
            x_depart += largeur + 0
        y_depart += 40

    y_depart = 400
    for i, (nom, duree, debut, fin, poids) in enumerate(taches):
        couleur = couleurs[i % len(couleurs)]  # Choisir une couleur
        largeur = duree * 10  # Exemple: 10 pixels par minute

        canvas.create_rectangle(x_depart, y_depart, x_depart + largeur, y_depart + hauteur, fill=couleur)
        canvas.create_text(x_depart + largeur/2, y_depart + hauteur/2, text=f"{nom} ({duree} min)", fill="white")
        x_depart += largeur + 0  # Déplacer le point de départ horizontal pour la prochaine tâche

    # Dessiner l'échelle horizontale
    echelle_y = y_depart + hauteur + 20  # Position de l'échelle sous les rectangles
    max_duree = sum(tache[1] for tache in taches)  # Durée totale des tâches
    x_echelle_depart = 50  # Point de départ de l'échelle
    x_echelle_fin = x_depart  # Point de fin de l'échelle

    # Dessiner une ligne horizontale pour l'échelle
    canvas.create_line(x_echelle_depart, echelle_y, x_echelle_fin, echelle_y, width=2)

    # Ajouter des tics tous les 10 minutes
    for i in range(0, max_duree + 10, 10):
        x_position = 50 + i * 10  # 10 pixels par minute
        canvas.create_line(x_position, echelle_y - 5, x_position, echelle_y + 5, width=2)
        canvas.create_text(x_position, echelle_y + 15, text=f"{round(i/10)} h", anchor=tk.N)

# Définir des tâches avec leurs durées (nom, durée, début, fin, poids)
taches = [
    ("Tâche A", 25, 0, 25, 1),
    ("Tâche B", 10, 25, 35, 2),
    ("Tâche C", 20, 5, 25, 2),
    ("Tâche D", 5, 0, 5, 1)
]

# Créer la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Ordonnancement des Tâches")

# Créer un canvas pour afficher les résultats sous forme de rectangles colorés
canvas = tk.Canvas(fenetre, width=800, height=300, bg="white")
canvas.pack(pady=0)

# Bouton pour déclencher l'affichage de l'ordonnancement
btn_afficher = tk.Button(fenetre, text="Afficher l'Ordonnancement", command=afficher_resultat)
btn_afficher.pack()

# Lancer la boucle principale de Tkinter
#fenetre.mainloop()

def ft(taches,cap):
    occ=[[] for i in range(cap)]
    taches=ordonnancement_taches(taches)
    case=[]
    for i, (nom, duree, debut, fin, poids) in enumerate(taches):
        for nb,cren in enumerate(occ):
            if len(cren)==0:
                case.append(nb)
            elif cren[-1][3]<=debut:   
                case.append(nb)
        if len(case)==0:
            print("oula")
            print((nom, duree, debut, fin, poids))
            return occ
        elif len(case)<poids:
            print("oula2")
            print((nom, duree, debut, fin, poids))
            return occ
        else:
            for p in range(poids):
                c=case[0]                
                occ[c].append(i)
                case.remove(c)
            case=[]
    return occ

print(ft(taches,3))