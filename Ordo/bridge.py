import collections
from ortools.sat.python import cp_model







def main() -> None:
    # Create the model.
    model = cp_model.CpModel()

    task_data = [(0, 3, 7, 1), (1, 2, 3, 1), (2, 2, 4, 1),(3, 3, 4, 2)]  # task = (animal_id, processing_time, due_date, weight)

    id_tasks=[i for i in range(len(task_data))]

    horizon = sum(task[1] for task in task_data)

    all_tasks = {}
    intervals=[]
    task_type = collections.namedtuple("task_type", "start end interval")

    for task_id, task in enumerate(task_data):
        animal_id, processing_time, due_date, weights= task
        suffix = f"_{task_id}"
        start_var = model.new_int_var(0, horizon, "start" + suffix)
        end_var = model.new_int_var(0, horizon, "end" + suffix)
        interval_var = model.new_interval_var(start_var, processing_time, end_var, "interval" + suffix)
        
        intervals.append(interval_var)
        all_tasks[task_id] = task_type(start=start_var, end=end_var, interval=interval_var)
        model.add(end_var<=due_date)

        
    

    


    

            


    # Objective: minimize the makespan.
    obj_var = model.new_int_var(0, horizon, "makespan")
    model.add_max_equality(
        obj_var,
        [all_tasks[task_id].end for task_id in all_tasks],
    )

    weights = [task[3] for task in task_data]


    model.add_cumulative(intervals, weights, 3)
    
    




    model.minimize(obj_var)

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    status = solver.solve(model)

    assigned_task_type = collections.namedtuple("assigned_task_type", "start id duration end")

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Solution:")
        # Create one list of assigned tasks per machine.
        assigned_tasks = collections.defaultdict(list)
        for task_id, task in enumerate(task_data):
            assigned_tasks[task_id].append(
                assigned_task_type(
                    start=solver.value(all_tasks[task_id].start),
                    id=task_id,
                    duration=task[1],
                    end=solver.value(all_tasks[task_id].start)+task[1],
                )
            )

        # Finally print the solution found.
        print("Optimal Schedule Length: ",round(solver.objective_value))
        for task_id in id_tasks:
            task = assigned_tasks[task_id][0]
            print(f"  Task {task.id}: Start at {task.start}, Duration {task.duration}")
    
    else:
        print("No solution found.")
    
    print("Time = ", solver.WallTime(), " milliseconds")

if __name__ == "__main__":
    main()
