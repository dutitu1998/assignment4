import numpy as np
from collections import deque

def least_cost_method(supply, demand, costs):
    allocation = np.zeros((len(supply), len(demand)), dtype=int)
    total_cost = 0
    remaining_supply = supply.copy()
    remaining_demand = demand.copy()

    while True:
        min_cost = float('inf')
        min_i, min_j = -1, -1

        for i in range(len(remaining_supply)):
            for j in range(len(remaining_demand)):
                if remaining_supply[i] > 0 and remaining_demand[j] > 0 and costs[i][j] < min_cost:
                    min_cost = costs[i][j]
                    min_i, min_j = i, j

        if min_i == -1:
            break

        quantity = min(remaining_supply[min_i], remaining_demand[min_j])
        allocation[min_i][min_j] = quantity
        remaining_supply[min_i] -= quantity
        remaining_demand[min_j] -= quantity
        total_cost += quantity * min_cost

    return allocation, total_cost

def find_loop(allocation, entering_cell):
    m, n = allocation.shape
    path = []
    stack = [(entering_cell, iter([(i, entering_cell[1]) for i in range(m) if i != entering_cell[0]] +
                                 [(entering_cell[0], j) for j in range(n) if j != entering_cell[1]]))]

    while stack:
        node, children = stack[-1]
        if node == entering_cell and len(path) > 1 and len(path) % 2 == 0:
            return path
        try:
            child = next(children)
            if allocation[child[0]][child[1]] > 0 or child == entering_cell:
                if child in path:
                    idx = path.index(child)
                    new_path = path[idx:] + [child]
                    if len(new_path) % 2 == 1:
                        continue
                    return new_path
                path.append(child)
                stack.append((child, iter([(i, child[1]) for i in range(m) if i != child[0] and (i != node[0] or child[1] != node[1])] +
                                         [(child[0], j) for j in range(n) if j != child[1] and (child[0] != node[0] or j != node[1])])))
        except StopIteration:
            if path:
                path.pop()
            stack.pop()

    return None

def modi_method(supply, demand, costs, initial_allocation):
    m, n = len(supply), len(demand)
    u = np.zeros(m)
    v = np.zeros(n)
    allocation = initial_allocation.copy()

    while True:
        # Step 1: Calculate dual variables
        u.fill(np.nan)
        v.fill(np.nan)
        u[0] = 0

        updated = True
        while updated:
            updated = False
            for i in range(m):
                for j in range(n):
                    if allocation[i][j] > 0:
                        if not np.isnan(u[i]) and np.isnan(v[j]):
                            v[j] = costs[i][j] - u[i]
                            updated = True
                        elif not np.isnan(v[j]) and np.isnan(u[i]):
                            u[i] = costs[i][j] - v[j]
                            updated = True

        # Step 2: Compute opportunity costs
        opportunity_cost = np.zeros((m, n))
        entering_cell = None
        min_opportunity_cost = 0

        for i in range(m):
            for j in range(n):
                if allocation[i][j] == 0:
                    opportunity_cost[i][j] = costs[i][j] - (u[i] + v[j])
                    if opportunity_cost[i][j] < min_opportunity_cost:
                        min_opportunity_cost = opportunity_cost[i][j]
                        entering_cell = (i, j)

        if min_opportunity_cost >= 0:
            break

        # Step 3: Find loop and adjust allocations
        loop = find_loop(allocation, entering_cell)
        if not loop:
            print("No loop found. Solution may be degenerate.")
            break

        min_q = min(allocation[cell[0]][cell[1]] for cell in loop[1::2])
        for idx, cell in enumerate(loop):
            if idx % 2 == 0:
                allocation[cell[0]][cell[1]] += min_q
            else:
                allocation[cell[0]][cell[1]] -= min_q

    total_cost = np.sum(allocation * costs)
    return allocation, total_cost

# Problem data
supply = np.array([200, 160, 90])
demand = np.array([180, 120, 150])
costs = np.array([
    [16, 20, 12],
    [14, 8, 18],
    [26, 24, 16]
])

# Step 1: Get initial solution
initial_allocation, initial_cost = least_cost_method(supply, demand, costs)
print("Initial Basic Feasible Solution (Least Cost Method):")
print("Allocation Matrix:")
print(initial_allocation)
print(f"Total Cost: {initial_cost} BDT\n")

# Step 2: Optimize using MODI Method
optimal_allocation, optimal_cost = modi_method(supply, demand, costs, initial_allocation)
print("Optimal Solution (MODI Method):")
print("Allocation Matrix:")
print(optimal_allocation)
print(f"Total Cost: {optimal_cost} BDT")