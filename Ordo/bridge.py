import collections
from ortools.sat.python import cp_model
import numpy as np


def plot_result():
    pass


def bridge_crossing_solve(data) :
    # Create the model.
    model = cp_model.CpModel()

    task_data=data[0]

    id_tasks=[i for i in range(len(task_data))]
    bridge_capacity=data[1]
    horizon = sum(task[1] for task in task_data)

    all_tasks = {}
    intervals=[]
    task_type = collections.namedtuple("task_type", "start end interval")

    for task_id, task in enumerate(task_data):
        processing_time, due_date, weights, before_list, after_list, set_date, name= task
        suffix = f"_{task_id}"
        start_var = model.new_int_var(0, horizon, "start" + suffix)
        end_var = model.new_int_var(0, horizon, "end" + suffix)
        interval_var = model.new_interval_var(start_var, processing_time, end_var, "interval" + suffix)
        
        intervals.append(interval_var)
        all_tasks[task_id] = task_type(start=start_var, end=end_var, interval=interval_var)
        if due_date!=None:
            model.add(end_var<=due_date)
        if set_date!=None:
            model.add(start_var>=set_date)


    for task_id, task in enumerate(task_data):
        before_list=task[3]
        after_list=task[4]
        for i in before_list:
            model.add(all_tasks[i].end<=all_tasks[task_id].end)
        for i in after_list:
            model.add(all_tasks[i].end>=all_tasks[task_id].end)


        
    
    # Objective: minimize the makespan.
    obj_var = model.new_int_var(0, horizon, "makespan")
    model.add_max_equality(
        obj_var,
        [all_tasks[task_id].end for task_id in all_tasks],
    )

    weights = [task[2] for task in task_data]


    model.add_cumulative(intervals, weights, bridge_capacity)
    
    




    model.minimize(obj_var)

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    status = solver.solve(model)

    assigned_task_type = collections.namedtuple("assigned_task_type", "start id duration end")

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        schedule=[]
        if VERBOSE>1:print("Solution:")
        # Create one list of assigned tasks per machine.
        assigned_tasks = collections.defaultdict(list)
        for task_id, task in enumerate(task_data):
            assigned_tasks[task_id].append(
                assigned_task_type(
                    start=solver.value(all_tasks[task_id].start),
                    id=task_id,
                    duration=task[0],
                    end=solver.value(all_tasks[task_id].start)+task[0],
                )
            )

        # Finally print the solution found.
        makespan=round(solver.objective_value)
        if VERBOSE>0:print("Optimal Schedule Length: ",makespan)
        for task_id in id_tasks:
            task = assigned_tasks[task_id][0]
            schedule.append((task_data[task_id][6],task.duration,task.start,task.end,task_data[task_id][2]))
            if VERBOSE>0:print(f"  Task {task.id}: Start at {task.start}, and end at  {task.end}, weight : {task_data[task_id][2]}")
    
    else:
        if VERBOSE>0:print("No solution found.")
        return(None,None,None)
    time=solver.WallTime()/1000
    if VERBOSE>0:print("Time = ", time, " seconds")
    return(time,schedule,makespan)


global VERBOSE
if __name__ == "__main__":
    
    VERBOSE=1

    task_data = [(3, 7, 1, [], [], 0, "ahah"), (2, 5, 1, [0, 3], [], 0, "ahah"), (2, 4, 1, [], [], 0, "ahah"),(3, 6, 2, [], [], 0, "ahah")]  # task = (processing_time, due_date, weight, before_list, after_list)
    #before_list = liste des taches qui doivent se terminer avant que celle là termine
    #after_list = liste des taches qui doivent se terminer après que celle là termine
    data=[task_data,3]
    bridge_crossing_solve(data)
else:
    VERBOSE=0