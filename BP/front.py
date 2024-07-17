import tkinter as tk
from tkinter import ttk
from time import sleep
from offline import generate_weights,create_data_model,fonction_tri,next_k_fit_offline
from BP import BP_exact

def personalise():
    
    
    def validate_param():
        
        size=int(spinbox_size.get())
        spinbox_size.destroy()
        label_size.destroy()

        capacity=int(spinbox_capacity.get())
        spinbox_capacity.destroy()
        label_capacity.destroy()

        submit_button.destroy()
        suite(size,capacity)
    
    def submit(size,capacity):
        global data
        weights=[]
        for i in range(size):
            val=spin[i].get()
            if val=="":
                val=0
            weights.append(int(val))
        data=create_data_model(size,capacity,weights)
        frame.destroy()
        create_initial_buttons()
    
    def suite(size,capacity):
        labels=[]
        for i in range(size):
            spinbox = ttk.Spinbox(frame, from_=0, to=capacity, width=5)
            spin.append(spinbox)
            spinbox.grid(row=i, column=1, padx=5, pady=5)
            
            label = ttk.Label(frame, text=f"item {i}")
            labels.append(label)
            label.grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            submit_button = ttk.Button(frame, text="Submit", command=lambda: submit(size,capacity))
            submit_button.grid(row=size+1, column=0,padx=5, columnspan=1, pady=10)
    spin=[]
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    spinbox_size = ttk.Spinbox(frame, from_=0, to=10, width=5)
    spinbox_size.grid(row=1, column=1, padx=5, pady=5)
    
    label_size = ttk.Label(frame, text="number of pieces")
    label_size.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)


    spinbox_capacity = ttk.Spinbox(frame, from_=0, to=10, width=5)
    spinbox_capacity.grid(row=2, column=1, padx=5, pady=5)
    
    label_capacity = ttk.Label(frame, text="bin capacity")
    label_capacity.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)


    submit_button = ttk.Button(frame, text="Submit", command=validate_param)
    submit_button.grid(row=3, column=0,padx=5, columnspan=1, pady=10)

    

    
def random_weight():
    def validate_param():
        global data
        param=[]
        for s in spins:
            if s.get()=="":
                param.append(None)
            else:
                param.append(int(s.get()))


        frame.destroy()
        distribution="normal"
        weights=generate_weights(param[0],param[1],param[2],param[3],param[4],param[5],distribution)
        data=create_data_model(param[0],param[1],weights)
        create_initial_buttons()

    param_text=["size", "max_capacity", "vmin","vmax","mean value of the weights", "standard deviation of the weights"]
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    spins=[]
    labels=[]
    distribution_text = "distribution"
    distribution="normal"
    for i,p in enumerate(param_text):
    

        spinbox = ttk.Spinbox(frame, from_=0, to=100, width=5)
        spinbox.grid(row=i, column=1, padx=5, pady=5)
        spins.append(spinbox)
    
        label = ttk.Label(frame, text=p)
        label.grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
        labels.append(label)


    submit_button = ttk.Button(frame, text="Submit", command=validate_param)
    submit_button.grid(row=len(param_text), column=0,padx=5, columnspan=1, pady=10)




def choose_preload():
    pass
def choose_load():
    
    def validate():
        mode["load"]=radio_var.get()
        
        sleep(0.1)
        
        for radio in lradio:
            try:
                radio.destroy()
            except NameError:
                pass

        button_valid.destroy()

        # Réafficher les boutons de départ
        if mode["load"]=="CUSTOM":
            personalise()
        elif mode["load"]=="RANDOM":
            random_weight()
        elif mode["load"]=="PRE-LOADED":
            choose_preload()
    
    

    # Suppression des boutons existants (assurez-vous qu'ils sont définis quelque part dans le code global)
    try:
        button_tree.destroy()
        button_graph.destroy()
        button_option.destroy()
    except NameError:
        pass

    lopt_name = ["RANDOM", "CUSTOM", "PRE-LOADED"]
    
    lradio = []
    radio_var = tk.StringVar(value=lopt_name[-1])  # Default selection

    for i, name in enumerate(lopt_name):
        radio = ttk.Radiobutton(root, text=name, variable=radio_var, value=name)
        lradio.append(radio)
        radio.pack(pady=10 * i)
    
    button_valid = ttk.Button(root, text="validate", command=validate)
    button_valid.pack(pady=10)

def calculate():
    print("data : ",data)
    num_bins,tps,bins,EMPTY=BP_exact(data)
    print("les objets : ",data["weights"],"ont été rangés dans ",num_bins," bins en ",tps/1000," secondes")
    print("voici la disposition des ",len(data["weights"]) ," objets dans les ",num_bins,"bins : ",bins)
    if EMPTY:
        print("le solver en a laissé au moins une vide...")
    pass

def choose_weight():
    pass
def choose_options():
    pass
def create_initial_buttons():
    

    global button_tree, button_graph,button_option
    button_tree = ttk.Button(root, text="Afficher les bins", command=calculate)
    button_tree.pack(pady=10)
    button_graph = ttk.Button(root, text="Choisir les items", command=choose_load)
    button_graph.pack(pady=0)
    button_option = ttk.Button(root, text="Choisir les options", command=choose_options)
    button_option.pack(pady=20)
mode = {"graphe": "POISSON", "tree": True, "verbose": 1, "space": False,"UI":True,"heuristique":False}



root = tk.Tk()
root.title("Interface avec Matplotlib")
# Création des boutons initiaux
create_initial_buttons()

# Lancement de la boucle principale
root.mainloop()