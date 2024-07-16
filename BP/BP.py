from ortools.linear_solver import pywraplp
#from offline import create_data_model,test_create_data_model,extract





def BP_exact(data,ub=None):
    if __name__ =="__main__":
        VERBOSE=2
    else:
        VERBOSE=0
    UB=ub
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver("SCIP")

    if not solver:
        return

    # Variables
    # x[i, j] = 1 if item i is packed in bin j.
    if UB!=None:
        data["bins"]=data["bins"][:UB]
    x = {}
    for i in data["items"]:
        for j in data["bins"]:
            x[(i, j)] = solver.IntVar(0, 1, "x_%i_%i" % (i, j))

    # y[j] = 1 if bin j is used.
    y = {}
    for j in data["bins"]:
        y[j] = solver.IntVar(0, 1, "y[%i]" % j)

    # Constraints
    # Each item must be in exactly one bin.
    for i in data["items"]:
        solver.Add(sum(x[i, j] for j in data["bins"]) == 1)

    # The amount packed in each bin cannot exceed its capacity.
    for j in data["bins"]:
        solver.Add(
            sum(x[(i, j)] * data["weights"][i] for i in data["items"])
            <= y[j] * data["bin_capacity"]
        )
    #solver.Add(sum(bin_usage) >= lower_bound)

    # Objective: minimize the number of bins used.
    solver.Minimize(solver.Sum([y[j] for j in data["bins"]]))

    if VERBOSE>0:print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL:
        print("Solution non-optimale trouvée.....")


    if status == pywraplp.Solver.OPTIMAL:
        bins=[]
        num_bins = 0
        for j in data["bins"]:
            if y[j].solution_value() == 1:
                bin_items = []
                bin_weight = 0
                for i in data["items"]:
                    if x[i, j].solution_value() > 0:
                        bin_items.append(i)
                        bin_weight += data["weights"][i]
                if bin_items:
                    num_bins += 1
                    if VERBOSE>0:
                        print("Bin number", j)
                        print("  Items packed:", bin_items)
                        print("  Total weight:", bin_weight,"\n")
                    bins.append(bin_items)
        if VERBOSE>0:
            print("Number of bins used:", data["bins"])
            print("Time = ", solver.WallTime(), " milliseconds")
    else:
        print("The problem does not have an optimal solution.")
    return num_bins,solver.WallTime(),bins


if __name__ == "__main__":
    data={}
    w=[1, 1, 3, 10, 6, 9, 6, 1, 7, 6]
    data["weights"] = w
    data["items"] = list(range(len(w)))
    data["bins"] = data["items"]
    data["bin_capacity"] = 12
    data={'weights': [1, 1, 3, 10, 6, 9, 6, 1, 7, 6, 12, 5, 9, 10, 14], 'items': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 'bins': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 'bin_capacity': 12}
    n=BP_exact(data)
    print(n)
    pass
 