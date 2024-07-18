import tkinter as tk
from tkinter import ttk
from time import sleep
from offline import next_fit_offline,generate_weights,create_data_model,fonction_tri,next_k_fit_offline,stat_an
from BP import BP_exact
import numpy as np

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
    def validate():
        global data
        mode["pre_load"]=radio_var.get()
        
        sleep(0.1)
        
        for radio in lradio:
            try:
                radio.destroy()
            except NameError:
                pass

        button_valid.destroy()
        create_initial_buttons()
        # Réafficher les boutons de départ
        if mode["pre_load"]=="30_hard_1":
            data=create_data_model(30,12,[2, 0, 7, 6, 5, 11, 8, 9, 3, 4, 8, 8, 0, 5, 4, 12, 7, 3, 10, 2, 8, 12, 2, 11, 1, 7, 7, 5, 0, 8])
        elif mode["pre_load"]=="30_hard_2":
            data=create_data_model(30,12,[7, 1, 4, 4, 11, 5, 12, 6, 10, 4, 7, 10, 7, 4, 9, 8, 0, 9, 4, 11, 9, 3, 8, 12, 10, 5, 1, 5, 5, 4])
        elif mode["pre_load"]=="10_easy":
            data=create_data_model(10,12,[7, 1, 4, 4, 11, 5, 12, 6, 10, 2])
            
    lopt_name = ["30_hard_1", "30_hard_2", "10_easy"]
    
    lradio = []
    radio_var = tk.StringVar(value=lopt_name[-1])  # Default selection

    for i, name in enumerate(lopt_name):
        radio = ttk.Radiobutton(root, text=name, variable=radio_var, value=name)
        lradio.append(radio)
        radio.pack(pady=10 * i)
    
    button_valid = ttk.Button(root, text="validate", command=validate)
    button_valid.pack(pady=10)
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
    if option["stat"]:
        stat=stat_an(data).copy()
    '''num_bins,tps,bins,EMPTY=BP_exact(data)
    print("les objets : ",data["weights"],"ont été rangés dans ",num_bins," bins en ",tps/1000," secondes")
    print("voici la disposition des ",len(data["weights"]) ," objets dans les ",num_bins,"bins : ",bins)
    '''


    print(f"{len(data["weights"])} weights : {data["weights"]}")
    if option["stat"]:
        print(f"stat : \n\t mean : {stat["mean"]}\n\t vmax : {stat["vmax"]}\n\t vmin : {stat["vmin"]}\n\t vmax : {stat["vmax"]}\n\t ecart type : {stat["std_dev"]}")
    
    if option["heuristique"]:
        up_bound={}
        up_bound["next_fit_offline"]=next_fit_offline(data)[0]
        #up_bound["best_fit_offline"]=best_fit_offline(data)[0]
        up_bound["next_k_fit_offline"]=next_k_fit_offline(data,round(data["bin_capacity"]/8))[0]###à modifier
        
        up_bound_sorted={}
        sorted_data=fonction_tri(data,decreasing=True)
        up_bound_sorted["next_fit_offline"]=next_fit_offline(sorted_data)[0]
        #up_bound_trie["best_fit_offline"]=best_fit_offline(sorted_data)[0]
        up_bound_sorted["next_k_fit_offline"]=next_k_fit_offline(sorted_data,round(data["bin_capacity"]/8))[0]###à modifier
        
        
        heur_text=["next_fit_offline","next_k_fit_offline"]
        best_bound=np.min([up_bound[i] for i in heur_text])
        best_bound_sorted=np.min(np.min([up_bound_sorted[i] for i in heur_text]))


        
        
        print("\n\t upper bounds found : ")
        for i in heur_text:
            print(f"{i} non triée: {up_bound[i]}")
            print(f"{i} triée: {up_bound_sorted[i]}")
        best_bound=min(best_bound,best_bound_sorted)
        print(f"best bound found : {best_bound}")
    
    

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



mode = {"load":None,"pre_load":None}
option={"heuristique":True,"stat":True}
data=create_data_model(10,12,[7, 1, 4, 4, 11, 5, 12, 6, 10, 2])


root = tk.Tk()
root.title("Interface avec Matplotlib")
# Création des boutons initiaux
create_initial_buttons()

# Lancement de la boucle principale
root.mainloop()