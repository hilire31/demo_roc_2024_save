import tkinter as tk
from tkinter import ttk
from bridge import bridge_crossing_solve, plot_result
from time import sleep




def resolve():
    def quit_resolve():
        frame.destroy()
        create_initial_buttons()

    if VERBOSE>0:
        print("task_data : ",data[0])
    button_tree.destroy()
    button_graph.destroy()
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    button_quit=ttk.Button(frame,text="quit",command=quit_resolve)
    button_quit.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)

    p=f"{len(task_data)} tasks"
    label_size = ttk.Label(frame, text=p)
    label_size.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    
    time,schedule,makespan=bridge_crossing_solve(data)
    if VERBOSE>0:
        print("schedule : ",schedule) #[(task.id,task.start,task.duration)]
        print("makespan : ",makespan)
        print("time : ",time)
    
    p=f"result : makespan = {makespan}"
    label_result = ttk.Label(frame, text=p)
    label_result.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)


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
        task_data=[]
        for i in range(size):

            val_dur=spin_duration[i].get()
            val_due=spin_due_date[i].get()
            val_weight=spin_weight[i].get()
            val_set=spin_set_date[i].get()


            
            if val_dur=="":
                val_dur=3
            if val_weight=="":
                val_weight=1
            if val_due=="":
                val_due=30
            if val_set=="":
                val_set=None
            else:
                val_set=int(val_set)
            task_data.append((int(val_dur),int(val_due),int(val_weight),[],[],val_set))
            data=[task_data,capacity]
        frame.destroy()
        create_initial_buttons()
    
    def suite(size,capacity):
        labels=[]
        param=['duration','due date','weight','set date']
        for i in range(len(param)):
            label = ttk.Label(frame, text=param[i])
            labels.append(label)
            label.grid(row=0, column=i+1, padx=5, pady=5, sticky=tk.W)
            
        for i in range(size):
            
            spindur = ttk.Spinbox(frame, from_=1, to=10, width=5)
            spin_duration.append(spindur)
            spindur.grid(row=i+1, column=1, padx=5, pady=5)

            spindue = ttk.Spinbox(frame, from_=0, to=30, width=5)
            spin_due_date.append(spindue)
            spindue.grid(row=i+1, column=2, padx=5, pady=5)

            spinbox = ttk.Spinbox(frame, from_=0, to=capacity, width=5)
            spin_weight.append(spinbox)
            spinbox.grid(row=i+1, column=3, padx=5, pady=5)

            spinset = ttk.Spinbox(frame, from_=0, to=30, width=5)
            spin_set_date.append(spinset)
            spinset.grid(row=i+1, column=4, padx=5, pady=5)


            label = ttk.Label(frame, text=f"item {i}")
            labels.append(label)
            label.grid(row=i+1, column=0, padx=5, pady=5, sticky=tk.W)
            submit_button = ttk.Button(frame, text="Submit", command=lambda: submit(size,capacity))
            submit_button.grid(row=size+1, column=0,padx=5, columnspan=1, pady=10)
    spin_weight=[]
    spin_duration=[]
    spin_due_date=[]
    spin_set_date=[]
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    spinbox_size = ttk.Spinbox(frame, from_=0, to=20, width=5)
    spinbox_size.grid(row=1, column=1, padx=5, pady=5)
    
    label_size = ttk.Label(frame, text="number of tasks")
    label_size.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)


    spinbox_capacity = ttk.Spinbox(frame, from_=0, to=10, width=5)
    spinbox_capacity.grid(row=2, column=1, padx=5, pady=5)
    
    label_capacity = ttk.Label(frame, text="bridge capacity")
    label_capacity.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)


    submit_button = ttk.Button(frame, text="Submit", command=validate_param)
    submit_button.grid(row=3, column=0,padx=5, columnspan=1, pady=10)






def choose_preload():
    def validate():
        global task_data
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
        if mode["pre_load"]=="II1":# task = (processing_time, due_date, weight, before_list, after_list)
            task_data=[(1, 7, 1, [], [], 0), (2, 5, 1, [0, 3], [], 0), (2, 4, 1, [], [], 0),(3, 6, 2, [], [], 0),(2, 8, 1, [0], [1], 0), (4, 18, 3, [], [], 0)]
        elif mode["pre_load"]=="ID1":
            task_data=[7, 1, 3, 4, 5, 6, 2, 7, 7, 4, 9, 8, 9, 4, 9, 5, 8, 3, 1, 5, 5, 7, 8, 9, 5, 4, 5, 3]
        elif mode["pre_load"]=="ID2":
            task_data=[7, 1, 3, 4, 5, 6, 2, 7, 7, 4, 9, 8, 9, 4, 9, 5, 8, 3, 1, 5, 5, 7, 8, 9, 5, 4, 5, 5]
        elif mode["pre_load"]=="IM1":
            task_data=[7, 1, 3, 4, 5, 6, 2, 7, 7, 4, 9, 8, 9, 4, 9, 3, 8]#, 5, 1, 5, 5
        elif mode["pre_load"]=="IS1":
            task_data=[(3, 7, 1, [], [], 0), (2, 5, 1, [0, 3], [], 0), (2, 4, 1, [], [], 0),(3, 6, 2, [], [], 0)]
        
    lopt_name = ["II1","ID1", "ID2", "IM1", "IS1"]
    
    lradio = []
    radio_var = tk.StringVar(value=lopt_name[-1])  # Default selection

    for i, name in enumerate(lopt_name):
        radio = ttk.Radiobutton(root, text=name, variable=radio_var, value=name)
        lradio.append(radio)
        radio.pack(pady=10 * i)
    
    button_valid = ttk.Button(root, text="validate", command=validate)
    button_valid.pack(pady=10)

def choose_tasks():
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
        elif mode["load"]=="PRE-LOADED":
            choose_preload()
    
    # Suppression des boutons existants (assurez-vous qu'ils sont définis quelque part dans le code global)
    try:
        button_tree.destroy()
        button_graph.destroy()
    except NameError:
        pass

    lopt_name = ["CUSTOM", "PRE-LOADED"]
    
    lradio = []
    radio_var = tk.StringVar(value=lopt_name[-1])  # Default selection

    for i, name in enumerate(lopt_name):
        radio = ttk.Radiobutton(root, text=name, variable=radio_var, value=name)
        lradio.append(radio)
        radio.pack(pady=10 * i)
    
    button_valid = ttk.Button(root, text="validate", command=validate)
    button_valid.pack(pady=10)






def create_initial_buttons():
    global button_tree, button_graph
    button_tree = ttk.Button(root, text="resolve the tasks order", command= resolve )
    button_tree.pack(pady=10)
    button_graph = ttk.Button(root, text="choose the tasks", command=choose_tasks)
    button_graph.pack(pady=0)


def main():
    global root,mode,task_data,data
    # Création de la fenêtre principale
    root = tk.Tk()
    root.title("Interface avec Matplotlib")
    mode = {"load":None,"pre_load":None}
    task_data = [(3, 7, 1, [], [], 0), (2, 5, 1, [0, 3], [], 0), (2, 4, 1, [], [], 0),(3, 6, 2, [], [], 0)]  # task = (processing_time, due_date, weight, before_list, after_list, set_date)
    #before_list = liste des taches qui doivent se terminer avant que celle là termine
    #after_list = liste des taches qui doivent se terminer après que celle là termine
    #set_date : date à laquelle la tache doit avoir commencé
    data=[task_data,3]
    # Création des boutons initiaux
    create_initial_buttons()

    # Lancement de la boucle principale
    root.mainloop()




global VERBOSE

VERBOSE=0


if __name__=="__main__":
    VERBOSE=1
    main()

