import tkinter as tk

def afficher_resultat(taches,canvas):
    # Effacer le contenu du canvas actuel
    canvas.delete("all")
    
    # Paramètres de dessin
    x_depart = 50  # Position de départ horizontale
    y_depart = 100
    espacement = 0  # Espace entre les rectangles
    last_x=[ 0 for i in range(len(taches)+max(poids for _, _, _, poids, _ in taches)+5)]
    # Couleurs des tâches
    couleurs = ["#FF6347", "#4682B4", "#32CD32", "#FFD700", "#FF69B4"]
    max_y=y_depart
    # Ajouter les rectangles colorés
    for i, ( duree, debut, fin, poids, nom) in enumerate(taches):
        couleur = couleurs[i % len(couleurs)]  # Choisir une couleur
        largeur = duree * 60  # Exemple: 60 pixels par heure
        hauteur = poids * 30  # Hauteur proportionnelle au poids (5 pixels par unité de poids)
        x_position = x_depart + debut * 60  # Position horizontale basée sur le début
        
        # Calculer la position verticale la plus proche où la tâche ne chevauche pas les autres
        for i,lastx in enumerate(last_x[0:-4]):
            if lastx <= x_position:
                if max(last_x[j] for j in range(i,i+poids))<=x_position:
                    y_position=y_depart+i*60
                    if y_position+poids*30 > max_y:
                        max_y=y_position+poids*30
                    for j in range(i,i+poids):
                        last_x[j]=x_position
                    break

        
        # Dessiner le rectangle représentant la tâche
        canvas.create_rectangle(x_position, y_position, x_position + largeur, y_position + hauteur, fill=couleur)
        
        # Ajouter le texte dans le rectangle
        canvas.create_text(x_position + largeur/2, y_position + hauteur/2, text=f"{nom}", fill="white")
        

    # Dessiner une échelle horizontale pour l'ensemble des tâches
    
    echelle_y =  max_y +10 # Position de l'échelle sous le dernier rectangle
    max_x = max(fin for _, _, fin, _, _ in taches)  # Durée totale des tâches pour ajuster l'échelle
    x_echelle_depart = 50  # Point de départ de l'échelle
    x_echelle_fin = x_echelle_depart + max_x * 60  # Point de fin de l'échelle

    # Dessiner une ligne horizontale pour l'échelle
    canvas.create_line(x_echelle_depart, echelle_y, x_echelle_fin, echelle_y, width=2)

    # Ajouter des tics tous les 10 minutes
    for i in range(0, max_x + 1, 1):
        x_position = x_echelle_depart + i * 60  # 10 pixels par minute
        canvas.create_line(x_position, echelle_y - 5, x_position, echelle_y + 5, width=2)
        canvas.create_text(x_position, echelle_y + 15, text=f"{i} heure", anchor=tk.N)



def main():
    # Définir des tâches avec leurs informations (nom, durée, début, fin, poids)
    taches = [
        ( 3, 0, 3, 3, "Tâche A"),
        ( 1, 4, 5, 2, "Tâche B"),
        ( 2, 3, 5, 1, "Tâche C"),
        ( 4, 5, 9, 1, "Tâche D")
    ]

    # Créer la fenêtre principale
    fenetre = tk.Tk()
    fenetre.title("Ordonnancement des Tâches")

    # Créer un canvas pour afficher les résultats sous forme de rectangles colorés
    canvas = tk.Canvas(fenetre, width=800, height=400, bg="white")
    canvas.pack(pady=20)

    # Bouton pour déclencher l'affichage de l'ordonnancement
    btn_afficher = tk.Button(fenetre, text="Afficher l'Ordonnancement", command=lambda: afficher_resultat(taches,canvas))
    btn_afficher.pack()

    # Lancer la boucle principale de Tkinter
    fenetre.mainloop()
if __name__=="__main__":
    main()