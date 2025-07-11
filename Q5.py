import numpy as np

def north_west_corner(supply, demand, costs):
    allocation = np.zeros((len(supply), len(demand)), dtype=int)
    i=0
    j=0
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

import numpy as np
def least_cost_method(supply, demand, costs):
    allocation = np.zeros((len(supply), len(demand)), dtype=int) #1st e allocation matrix 0,0 kore newa hoiche
    total_cost = 0
    remaining_supply = supply.copy() #original supply,demand will not changeable
    remaining_demand = demand.copy()  #same statement

    while True: #since in least cost method we dont know how many loops will required.so we take infinitive loop
        # Find the cell with the minimum cost among remaining cells
        min_cost = float('inf') #float('inf') == ∞ so what we taken will always be greater
        min_i, min_j = -1, -1 #-1 means no valid cell found

        for i in range(len(remaining_supply)): #loop over every source indices
            for j in range(len(remaining_demand)):#loop over every destination indices
                #source i still has supply left,destination j needs unit and this cell cost is lower then any other cell
                if remaining_supply[i] > 0 and remaining_demand[j] > 0 and costs[i][j] < min_cost: 
                    #so this cell has the minimum cost
                    min_cost = costs[i][j]
                    min_i, min_j =i, j   #so this is the minimum cell
#if this occurence did not happen then or this can happen when no mre cell left then 
        if min_i == -1: 
            break
#we have selected minimum cell but same minimum value can be seen in multiple cell so how to clear this problem
        quantity = min(remaining_supply[min_i], remaining_demand[min_j])
        allocation[min_i][min_j] = quantity #we are allocating this quantity into the cell 
        remaining_supply[min_i] -= quantity #now we have to subtract like north_west corner method
        remaining_demand[min_j] -= quantity  #same statement
        total_cost += quantity * min_cost  #now sum all the things

    return allocation, total_cost


# Problem data
supply = np.array([80, 60, 40, 20])
demand = np.array([60, 60, 30, 40, 10])
costs = np.array([ [4, 3, 1, 2, 6],[5, 2, 3, 4, 5], [3, 5, 6, 3, 2],  [2, 4, 4, 5, 3]])

# North-West Corner Rule
print("North-West Corner Rule:")
nw_allocation, nw_cost = north_west_corner(supply.copy(), demand.copy(), costs) #call function
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