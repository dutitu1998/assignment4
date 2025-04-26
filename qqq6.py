import numpy as np

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

def modi_method(supply, demand, costs, allocation):
    m, n = allocation.shape
    while True:
        u, v = np.full(m, np.nan), np.full(n, np.nan)
        u[0] = 0
        updated = True
        while updated:
            updated = False
            for i in range(m):
                for j in range(n):
                    if allocation[i, j] > 0:
                        if np.isnan(u[i]) and not np.isnan(v[j]):
                            u[i] = costs[i, j] - v[j]
                            updated = True
                        elif not np.isnan(u[i]) and np.isnan(v[j]):
                            v[j] = costs[i, j] - u[i]
                            updated = True

        opportunity = np.where(allocation == 0, costs - u[:, None] - v, np.inf)
        if np.all(opportunity >= 0):
            break
        i, j = np.unravel_index(np.argmin(opportunity), opportunity.shape)
        
        def find_loop(allocation, start):
            m, n = allocation.shape
            stack = [(start, [])]
            while stack:
                (x, y), path = stack.pop()
                if len(path) >= 4 and (x, y) == start and len(path) % 2 == 0:
                    return path
                next_moves = [(i, y) for i in range(m) if allocation[i, y] > 0 or (i, y) == start] + \
                             [(x, j) for j in range(n) if allocation[x, j] > 0 or (x, j) == start]
                for move in next_moves:
                    if move not in path:
                        stack.append((move, path + [move]))
            return None
        
        loop = find_loop(allocation, (i, j))
        q = min(allocation[x, y] for idx, (x, y) in enumerate(loop[1::2]))
        for idx, (x, y) in enumerate(loop):
            allocation[x, y] += q if idx % 2 == 0 else -q

    total_cost = (allocation * costs).sum()
    return allocation, total_cost

# Problem data
supply = np.array([200, 160, 90])
demand = np.array([180, 120, 150])
costs = np.array([[16, 20, 12], [14, 8, 18], [26, 24, 16]])

# Solve
initial_allocation, initial_cost = least_cost_method(supply, demand, costs)
print("Initial Basic Feasible Solution (Least Cost Method):")
print("Allocation Matrix:\n", initial_allocation)
print(f"Total Cost: {initial_cost} BDT\n")

optimal_allocation, optimal_cost = modi_method(supply, demand, costs, initial_allocation.copy())
print("Optimal Solution (MODI Method):")
print("Allocation Matrix:\n", optimal_allocation)
print(f"Total Cost: {optimal_cost} BDT")
