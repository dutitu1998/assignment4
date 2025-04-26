import numpy as np
from scipy.optimize import linear_sum_assignment
profit_matrix = np.array([[16, 10, 14, 11], [14, 11, 15, 15], [15, 15, 13, 12],[13, 12, 14, 15]])

# Step 1: Convert the profit matrix to a cost matrix for maximization
# Since the Hungarian algorithm minimizes cost, we convert profits
cost_matrix = np.max(profit_matrix) - profit_matrix

# Step 2: Apply the Hungarian algorithm to find the optimal assignment
row_ind, col_ind = linear_sum_assignment(cost_matrix)

# Step 3: Map assignments to corresponding salesman and city
salesmen = ['A', 'B', 'C', 'D']
assignments = [(salesmen[i], col + 1) for i, col in enumerate(col_ind)]

# Step 4: Calculate the total maximum profit based on optimal assignment
total_profit = profit_matrix[row_ind, col_ind].sum()
print("Optimal Assignments:")
for salesman, city in assignments:
    print(f"Salesman {salesman} → City {city}")

print(f"Total Maximum Profit: {total_profit} BDT")
