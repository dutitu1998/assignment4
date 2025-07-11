import numpy as np

# -----------------------------------------------------------------
# Vogel’s Approximation Method (VAM)
# -----------------------------------------------------------------
def vogel_method(supply, demand, costs):
    allocation = np.zeros((len(supply), len(demand)), dtype=int)
    total_cost = 0
    remaining_supply = supply.copy()
    remaining_demand = demand.copy()

    while True:
        # ------ compute row penalties ------
        row_penalty = []
        for i in range(len(remaining_supply)):
            if remaining_supply[i] == 0:
                row_penalty.append(-1)
                continue
            active_costs = [costs[i][j] for j in range(len(remaining_demand)) if remaining_demand[j] > 0]
            if len(active_costs) < 2:
                row_penalty.append(0)
            else:
                cheapest, second_cheapest = sorted(active_costs)[:2]
                row_penalty.append(second_cheapest - cheapest)

        # ------ compute column penalties ------
        col_penalty = []
        for j in range(len(remaining_demand)):
            if remaining_demand[j] == 0:
                col_penalty.append(-1)
                continue
            active_costs = [costs[i][j] for i in range(len(remaining_supply)) if remaining_supply[i] > 0]
            if len(active_costs) < 2:
                col_penalty.append(0)
            else:
                cheapest, second_cheapest = sorted(active_costs)[:2]
                col_penalty.append(second_cheapest - cheapest)

        # ------ stop if everything is allocated ------
        if max(row_penalty) == -1 and max(col_penalty) == -1:
            break

        # ------ choose the row or column with the largest penalty ------
        if max(row_penalty) >= max(col_penalty):
            i = row_penalty.index(max(row_penalty))
            # pick cheapest cost in that row
            j = min([j for j in range(len(remaining_demand)) if remaining_demand[j] > 0],
                    key=lambda j: costs[i][j])
        else:
            j = col_penalty.index(max(col_penalty))
            # pick cheapest cost in that column
            i = min([i for i in range(len(remaining_supply)) if remaining_supply[i] > 0],
                    key=lambda i: costs[i][j])

        # ------ allocate as much as possible ------
        quantity = min(remaining_supply[i], remaining_demand[j])
        allocation[i][j] = quantity
        total_cost += quantity * costs[i][j]
        remaining_supply[i] -= quantity
        remaining_demand[j] -= quantity

    return allocation, total_cost


# -----------------------------------------------------------------
# Problem data
# -----------------------------------------------------------------
supply = np.array([80, 60, 40, 20])
demand = np.array([60, 60, 30, 40, 10])
costs  = np.array([[4, 3, 1, 2, 6],
                   [5, 2, 3, 4, 5],
                   [3, 5, 6, 3, 2],
                   [2, 4, 4, 5, 3]])

# -----------------------------------------------------------------
# Run the three methods
# -----------------------------------------------------------------


print("Vogel’s Approximation Method:")
vam_alloc, vam_cost = vogel_method(supply.copy(), demand.copy(), costs)
print(vam_alloc); print("Total Cost:", vam_cost)
