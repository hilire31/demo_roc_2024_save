import tkinter as tk
from tkinter import ttk
from VCover import BnB_vertex, load_graph,plotgraph
from time import sleep
from personalise import fill_graph

# Fonction pour créer et afficher l'arbre des états


def personalise():
    spin=[]
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    types=["carnivores",
        "herbivores",
        "vegetals",
        "omnivores",
        "grains"]
    labels=[]
    for i in range(len(types)):
        spinbox = ttk.Spinbox(frame, from_=0, to=10, width=5)
        spin.append(spinbox)
        spinbox.grid(row=i, column=1, padx=5, pady=5)
        label = ttk.Label(frame, text=types[i])
        labels.append(label)
        label.grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
    def submit():
        global amount
        amount={}
        for i in range(len(types)):
            val=spin[i].get()
            if val=="":
                val=0
            amount[types[i]]=int(val)
        G=fill_graph(amount)
        frame.destroy()
        create_initial_buttons()

    submit_button = ttk.Button(frame, text="Submit", command=submit)
    submit_button.grid(row=len(types)+1, column=0,padx=5, columnspan=1, pady=10)
    








def choose_graph():
    
    def validate():
        mode["graphe"]=radio_var.get()
        
        sleep(0.1)
        
        for radio in lradio:
            try:
                radio.destroy()
            except NameError:
                pass

        button_valid.destroy()

        # Réafficher les boutons de départ
        if mode["graphe"]!="PERSO":
            create_initial_buttons()
        else:
            personalise()
    
    def create_initial_buttons():
        global button_tree, button_graph
        button_tree = ttk.Button(root, text="Afficher l'Arbre des États", command=plot_state_tree)
        button_tree.pack(pady=10)
        button_graph = ttk.Button(root, text="Choose the graph", command=choose_graph)
        button_graph.pack(pady=0)

    # Suppression des boutons existants (assurez-vous qu'ils sont définis quelque part dans le code global)
    try:
        button_tree.destroy()
        button_graph.destroy()
    except NameError:
        pass

    lopt_name = ["KARATE", "US", "MAISON", "POISSON", "TEST","PERSO"]
    
    lradio = []
    radio_var = tk.StringVar(value=lopt_name[-1])  # Default selection

    for i, name in enumerate(lopt_name):
        radio = ttk.Radiobutton(root, text=name, variable=radio_var, value=name)
        lradio.append(radio)
        radio.pack(pady=10 * i)
    
    button_valid = ttk.Button(root, text="validate", command=validate)
    button_valid.pack(pady=10)

def plot_state_tree():
    pass
    # Exemple simple d'arbre des états sous forme de graphique
    
    # Set appropriate flags
    if mode["graphe"]!="PERSO":
        G = load_graph(mode)
    else:
        G=fill_graph(amount)
        #labels = {i: G.nodes[i]["name"] for i in range(amount["tot"])}
    vertex_cover_min, state_tree, nb_iter,frame = BnB_vertex(G, mode)
    figure=plotgraph(G)

    
    
    


def create_initial_buttons():
    global button_tree, button_graph
    button_tree = ttk.Button(root, text="Afficher l'Arbre des États", command=plot_state_tree)
    button_tree.pack(pady=10)
    button_graph = ttk.Button(root, text="Choose the graph", command=choose_graph)
    button_graph.pack(pady=0)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Interface avec Matplotlib")

# Création d'un frame pour contenir le graphique
mode = {"graphe": "POISSON", "tree": True, "verbose": 1, "space": False,"UI":True,"heuristique":False}
amount={
        "carnivores":3,
        "herbivores":2,
        "vegetals":1,
        "omnivores":2,
        "grains":1,
        "tot":8,
    }
# Création des boutons initiaux
create_initial_buttons()

# Lancement de la boucle principale
root.mainloop()
