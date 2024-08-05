import collections
from ortools.sat.python import cp_model




def count_occurrences(items):
    """
    Compte le nombre d'occurrences de chaque objet dans une liste et renvoie une liste
    de tuples contenant l'objet et son nombre d'occurrences.

    Args:
        items (list): La liste des objets à compter.

    Returns:
        list of tuple: Une liste de tuples où chaque tuple contient un objet et son nombre d'occurrences.
    """
    counter = collections.Counter(items)
    return list(counter.items())



def main() -> None:
    # Create the model.
    model = cp_model.CpModel()

    task_data = [(0, 3, 7, 1), (1, 2, 8, 1), (2, 2, 9, 1)]  # task = (animal_id, processing_time, due_date, weight)
    machines = [(0, 2), (1, 1)]  # machine = (boat_id, capacity)
    nb_machines = len(machines)
    id_tasks=[i for i in range(len(task_data))]
    id_machines = [machine[0] for machine in machines]
    capacities = {machine[0]: machine[1] for machine in machines}

    horizon = sum(task[1] for task in task_data)

    all_tasks = {}
    machine_to_intervals = collections.defaultdict(list)
    machine_id_to_intervals=collections.defaultdict(list)
    intervals=[]
    task_type = collections.namedtuple("task_type", "start end interval machine_used")

    for task_id, task in enumerate(task_data):
        animal_id, processing_time, due_date, weights= task
        suffix = f"_{task_id}"
        start_var = model.new_int_var(0, horizon, "start" + suffix)
        end_var = model.new_int_var(0, horizon, "end" + suffix)
        interval_var = model.new_interval_var(start_var, processing_time, end_var, "interval" + suffix)
        
        intervals.append(interval_var)
        machine_var = model.new_int_var_from_domain(cp_model.Domain.FromValues(id_machines), "machine" + suffix)
        all_tasks[task_id] = task_type(start=start_var, end=end_var, interval=interval_var, machine_used=machine_var)
        model.add(end_var<=due_date)
        machine_to_intervals[machine_var].append(interval_var)
        for id in id_machines:
            machine_id_to_intervals[id].append(interval_var)

        

    # Add no-overlap constraint for each machine.
    
    for machine in id_machines:
        model.add_no_overlap(machine_id_to_intervals[machine])
    


    weights = [task[3] for task in task_data]

    for machine in id_machines:
        model.add_cumulative(machine_to_intervals[machine], weights, 3)
    #model.add_cumulative(intervals, weights, 2)

    # Add capacity constraints.
    '''
    for machine_id in id_machines:
        assigned_tasks = [model.new_bool_var(f"assigned_{task_id}_to_{machine_id}") for task_id in all_tasks]
        for task_id, task in enumerate(task_data):
            model.add(
                all_tasks[task_id].machine_used == machine_id
            ).only_enforce_if(assigned_tasks[task_id])
            model.add(
                all_tasks[task_id].machine_used != machine_id
            ).only_enforce_if(assigned_tasks[task_id].Not())
    '''
    

            


    # Objective: minimize the makespan.
    obj_var = model.new_int_var(0, horizon, "makespan")
    model.add_max_equality(
        obj_var,
        [all_tasks[task_id].end for task_id in all_tasks],
    )
    
    




    model.minimize(obj_var)

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    status = solver.solve(model)

    assigned_task_type = collections.namedtuple("assigned_task_type", "start job index duration machine")

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Solution:")
        # Create one list of assigned tasks per machine.
        assigned_tasks = collections.defaultdict(list)
        for task_id, task in enumerate(task_data):
            machine_used = solver.value(all_tasks[task_id].machine_used)
            assigned_tasks[machine_used].append(
                assigned_task_type(
                    start=solver.value(all_tasks[task_id].start),
                    job=task_id,
                    index=task_id,
                    duration=task[1],
                    machine=machine_used
                )
            )

        # Finally print the solution found.
        #print(f"Optimal Schedule Length: {solver.objective_value()}")
        for machine in id_machines:
            assigned_tasks[machine].sort()
            print(f"Machine {machine}:")
            for task in assigned_tasks[machine]:
                print(f"  Task {task.index}: Start at {task.start}, Duration {task.duration}")

    else:
        print("No solution found.")
    print(machine_to_intervals)
    print("Time = ", solver.WallTime(), " milliseconds")

if __name__ == "__main__":
    main()
