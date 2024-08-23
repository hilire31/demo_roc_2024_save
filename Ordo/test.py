import tkinter as tk

def afficher_resultat(taches,canvas):
    # Effacer le contenu du canvas actuel
    canvas.delete("all")
    
    # Paramètres de dessin
    x_depart = 50  # Position de départ horizontale
    espacement = 0  # Espace entre les rectangles
    y_positions = []  # Liste pour stocker les positions verticales des tâches

    # Couleurs des tâches
    couleurs = ["#FF6347", "#4682B4", "#32CD32", "#FFD700", "#FF69B4"]

    # Ajouter les rectangles colorés
    for i, ( nom, duree, debut, fin, poids) in enumerate(taches):
        couleur = couleurs[i % len(couleurs)]  # Choisir une couleur
        largeur = duree * 10  # Exemple: 10 pixels par minute
        hauteur = poids * 30  # Hauteur proportionnelle au poids (5 pixels par unité de poids)
        x_position = x_depart + debut * 10  # Position horizontale basée sur le début
        
        # Calculer la position verticale la plus proche où la tâche ne chevauche pas les autres
        y_position = 100
        for y_existing, fin_existing, hauteur_existing in y_positions:
            if (x_position + largeur > x_depart + fin_existing * 10) or (x_position > x_depart + fin_existing * 10):
                continue
            y_position = max(y_position, y_existing + hauteur_existing + espacement)
        
        # Enregistrer la position verticale et la fin de la tâche actuelle
        y_positions.append((y_position, fin, hauteur))
        
        # Dessiner le rectangle représentant la tâche
        canvas.create_rectangle(x_position, y_position, x_position + largeur, y_position + hauteur, fill=couleur)
        
        # Ajouter le texte dans le rectangle
        canvas.create_text(x_position + largeur/2, y_position + hauteur/2, text=f"{nom}", fill="white")
        

    # Dessiner une échelle horizontale pour l'ensemble des tâches
    echelle_y = max(y for y, _, _ in y_positions) + 40  # Position de l'échelle sous le dernier rectangle
    max_duree = max(fin for _, _, _, fin, _ in taches)  # Durée totale des tâches pour ajuster l'échelle
    x_echelle_depart = 50  # Point de départ de l'échelle
    x_echelle_fin = x_echelle_depart + max_duree * 10  # Point de fin de l'échelle

    # Dessiner une ligne horizontale pour l'échelle
    canvas.create_line(x_echelle_depart, echelle_y, x_echelle_fin, echelle_y, width=2)

    # Ajouter des tics tous les 10 minutes
    for i in range(0, max_duree + 10, 10):
        x_position = x_echelle_depart + i * 10  # 10 pixels par minute
        canvas.create_line(x_position, echelle_y - 5, x_position, echelle_y + 5, width=2)
        canvas.create_text(x_position, echelle_y + 15, text=f"{i} min", anchor=tk.N)



def main():
    # Définir des tâches avec leurs informations (nom, durée, début, fin, poids)
    taches = [
        ("Tâche A", 30, 0, 30, 3),
        ("Tâche B", 10, 35, 45, 2),
        ("Tâche C", 20, 10, 30, 1),
        ("Tâche D", 5, 50, 55, 1)
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