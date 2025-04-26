import numpy as np

def north_west_corner(supply, demand, costs):
    allocation = np.zeros((len(supply), len(demand)), dtype=int)
    i, j = 0, 0
    total_cost = 0

    while i < len(supply) and j < len(demand):
        quantity = min(supply[i], demand[j])
        allocation[i][j] = quantity
        supply[i] -= quantity
        demand[j] -= quantity
        total_cost += quantity * costs[i][j]

        if supply[i] == 0:
            i += 1
        else:
            j += 1

    return allocation, total_cost

def least_cost_method(supply, demand, costs):
    allocation = np.zeros((len(supply), len(demand)), dtype=int)
    total_cost = 0
    remaining_supply = supply.copy()
    remaining_demand = demand.copy()

    while True:
        # Find the cell with the minimum cost among remaining cells
        min_cost = float('inf')
        min_i, min_j = -1, -1

        for i in range(len(remaining_supply)):
            for j in range(len(remaining_demand)):
                if remaining_supply[i] > 0 and remaining_demand[j] > 0 and costs[i][j] < min_cost:
                    min_cost = costs[i][j]
                    min_i, min_j = i, j

        if min_i == -1:  # No more cells to allocate
            break

        quantity = min(remaining_supply[min_i], remaining_demand[min_j])
        allocation[min_i][min_j] = quantity
        remaining_supply[min_i] -= quantity
        remaining_demand[min_j] -= quantity
        total_cost += quantity * min_cost

    return allocation, total_cost

# Problem data
supply = np.array([80, 60, 40, 20])
demand = np.array([60, 60, 30, 40, 10])
costs = np.array([ [4, 3, 1, 2, 6],[5, 2, 3, 4, 5], [3, 5, 6, 3, 2],  [2, 4, 4, 5, 3]])

# North-West Corner Rule
print("North-West Corner Rule:")
nw_allocation, nw_cost = north_west_corner(supply.copy(), demand.copy(), costs)
print("Allocation Matrix:")
print(nw_allocation)
print("Total Cost:", nw_cost)
print()
# Least Cost Method
print("Least Cost Method:")
lc_allocation, lc_cost = least_cost_method(supply.copy(), demand.copy(), costs)
print("Allocation Matrix:")
print(lc_allocation)
print("Total Cost:", lc_cost)