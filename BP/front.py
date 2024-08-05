import tkinter as tk
from tkinter import ttk
from time import sleep
from offline import next_fit_offline,generate_weights,create_data_model,fonction_tri,next_k_fit_offline,stat_an,best_fit_offline
from BP import BP_exact
import numpy as np

data=create_data_model(10,12,[7, 1, 3, 4, 5, 6, 2, 7, 7 ,4])
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

        if param[2]==None:
            param[2]=0
        if param[3]==None:
            param[3]=100


        frame.destroy()
        distribution="normal"
        weights=generate_weights(param[0],param[1],round(param[1]*param[2]/100),round(param[1]*param[3]/100),param[4],param[5],distribution)
        data=create_data_model(param[0],param[1],weights)
        create_initial_buttons()

    param_text=["size", "max_capacity", "vmin en '%' de la cap","vmax en '%' de la cap","mean value of the weights", "standard deviation of the weights"]
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
        if mode["pre_load"]=="II1":
            w=[7, 1, 3, 4, 5, 6, 2, 7, 7, 4, 3, 1, 5, 5, 7, 10, 9, 5, 4, 5, 3, 6, 2, 7, 7, 11, 9, 8, 4, 5, 3, 6, 2, 7, 7, 11, 9, 8]
            data=create_data_model(len(w),12,w)
        elif mode["pre_load"]=="ID1":
            d=[7, 1, 3, 4, 5, 6, 2, 7, 7, 4, 9, 8, 9, 4, 9, 5, 8, 3, 1, 5, 5, 7, 8, 9, 5, 4, 5, 3]
            data=create_data_model(len(d),12,d)
        elif mode["pre_load"]=="ID2":
            d=[7, 1, 3, 4, 5, 6, 2, 7, 7, 4, 9, 8, 9, 4, 9, 5, 8, 3, 1, 5, 5, 7, 8, 9, 5, 4, 5, 5]
            data=create_data_model(len(d),12,d)
        elif mode["pre_load"]=="IM1":
            w=[7, 1, 3, 4, 5, 6, 2, 7, 7, 4, 9, 8, 9, 4, 9, 3, 8]#, 5, 1, 5, 5
            data=create_data_model(len(w),12,w)
        elif mode["pre_load"]=="IS1":
            data=create_data_model(10,12,[7, 1, 3, 4, 7, 6, 2, 5, 7 ,4])
        
    lopt_name = ["II1","ID1", "ID2", "IM1", "IS1"]
    
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

def create_heuristique(data):
    up_bound_bins={}
    up_bound={}
    up_bound["next_fit_offline"]=next_fit_offline(data)[0]
    up_bound_bins["next_fit_offline"]=next_fit_offline(data)[2]
    up_bound["best_fit_offline"]=best_fit_offline(data)[0]
    up_bound_bins["best_fit_offline"]=best_fit_offline(data)[2]
    up_bound["next_k_fit_offline"]=next_k_fit_offline(data,round(data["bin_capacity"]/8))[0]###à modifier
    up_bound_bins["next_k_fit_offline"]=next_k_fit_offline(data,round(data["bin_capacity"]/8))[2]###à modifier


    up_bound_sorted={}
    up_bound_sorted_bins={}
    sorted_data=data.copy()
    fonction_tri(sorted_data,decreasing=True)
    up_bound_sorted["next_fit_offline"]=next_fit_offline(sorted_data)[0]
    up_bound_sorted_bins["next_fit_offline"]=next_fit_offline(sorted_data)[2]
    up_bound_sorted["best_fit_offline"]=best_fit_offline(sorted_data)[0]
    up_bound_sorted_bins["best_fit_offline"]=best_fit_offline(sorted_data)[2]
    up_bound_sorted["next_k_fit_offline"]=next_k_fit_offline(sorted_data,round(data["bin_capacity"]/8))[0]###à modifier
    up_bound_sorted_bins["next_k_fit_offline"]=next_k_fit_offline(sorted_data,round(data["bin_capacity"]/8))[2]###à modifier
    
    
    heur_text=["next_fit_offline","next_k_fit_offline","best_fit_offline"]
    best_bound=np.min([up_bound[i] for i in heur_text])
    best_bound_sorted=np.min(np.min([up_bound_sorted[i] for i in heur_text]))

    h={}
    h["best_bound"]=min(best_bound,best_bound_sorted,)
    for i in heur_text:
        h[f"{i}_non_triée"]=up_bound[i]
        h[f"{i}_non_triée_bins"]=up_bound_bins[i]
        h[f"{i}_triée"]=up_bound_sorted[i]
        h[f"{i}_triée_bins"]=up_bound_sorted_bins[i]

    return h.copy()


def calculate():
    def aff_stat(stat,button):
        button.destroy()
        p="stat : "
        p+=f"\n\t number of weights : {stat['size']} \n\t lower bound : {stat['lb']} \n\t bin capacity : {stat['bin_capacity']}"
        p+=f"\n\t number of packings : {stat['brute_force']}"
        p+=f"\n\t mean : {stat['mean']}\n\t vmax : {stat['vmax']}\n\t vmin : {stat['vmin']}\n\t vmax : {stat['vmax']}\n\t ecart type : {stat['std_dev']}"
        
        label_size = ttk.Label(frame, text=p)
        label_size.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    
    def aff_heur(heur,buttons):
        for i in buttons:
            i.destroy()
        p=""
        for i in heur:
            p+=i+" : "
            p+=str(heur[i])+"\n" 
        print(p)
        label_size = ttk.Label(frame, text=p)
        label_size.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

    def calc(data,ub=None):
        def thread_calc(data):
            global nb_bins,tps,bins,empty
            nb_bins,tps,bins,empty=BP_exact(data)
        
        def thread_calc_ub(data,ub):
            global nb_bins,tps,bins,empty
            nb_bins,tps,bins,empty=BP_exact(data,ub)
        if ub==None:
            nb_bins,tps,bins,empty=BP_exact(data)
            t=f"the items have been packed in {nb_bins} bins in {tps/1000} seconds"
            t+=f"\n the final bins are {bins}"

            bins_weights=[]
            bin_weights=[]
            for bin in bins:
                for i in bin:
                    bin_weights.append(data['weights'][i])
                bins_weights.append(bin_weights)
                bin_weights=[]
            t+=f"\n in weights : {bins_weights}"

            label_result = ttk.Label(frame_choice, text=t)
            label_result.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        else:
            nb_bins,tps,bins,empty=BP_exact(data,ub)
            t=f"the items have been packed in {nb_bins} bins in {tps/1000} seconds thanks to the upper bound"
            t+=f"\n the final bins are {bins}"

            bins_weights=[]
            bin_weights=[]
            for bin in bins:
                for i in bin:
                    bin_weights.append(data["weights"][i])
                bins_weights.append(bin_weights)
                bin_weights=[]
            t+=f"\n in weights : {bins_weights}"

            label_result = ttk.Label(frame_choice, text=t)
            label_result.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
    def quit():
        frame_choice.destroy()
        frame.destroy()
        create_initial_buttons()
        
    stat=stat_an(data).copy()
    buttons=[button_tree, button_graph,button_option]
    for i in buttons:
        i.destroy()
    
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    p=f"{len(data['weights'])} weights : {data['weights']}"
    label_size = ttk.Label(frame, text=p)
    label_size.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    print(f"{len(data['weights'])} weights : {data['weights']}")

    button_stat=ttk.Button(frame,text="Stat", command=lambda:aff_stat(stat,button_stat))
    button_stat.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    heur=create_heuristique(data).copy()
    button_heur=ttk.Button(frame,text="Heuristique", command=lambda:aff_heur(heur,[button_stat,button_heur]))
    button_heur.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
    
    frame_choice = ttk.Frame(root, padding="10")
    frame_choice.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    button_UB=ttk.Button(frame_choice,text="Upper Bound", command=lambda:calc(data,heur["best_bound"]))
    button_UB.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
    

    button_nUB=ttk.Button(frame_choice,text="No Upper Bound", command=lambda:calc(data))
    button_nUB.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

    quit_button=ttk.Button(frame_choice,text="Quit", command=quit)
    quit_button.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)
    

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


root = tk.Tk()
root.title("Interface avec Matplotlib")
# Création des boutons initiaux
create_initial_buttons()

# Lancement de la boucle principale
root.mainloop()