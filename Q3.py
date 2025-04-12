from pulp import *

# Create the problem
prob = LpProblem("Coal_Blending_Optimization", LpMaximize)

# Define the decision variables
x_A = LpVariable("Coal_A", 0, None)  # Tons of Coal A
x_B = LpVariable("Coal_B", 0, None)  # Tons of Coal B
x_C = LpVariable("Coal_C", 0, None)  # Tons of Coal C

# Define the objective function (maximize profit)
prob += 12*x_A + 15*x_B + 14*x_C, "Total_Profit"

# Add constraints
# 1. Total fuel constraint (up to 100 tons)
prob += x_A + x_B + x_C <= 100, "Total_Fuel"

# 2. Phosphorous constraint (≤ 0.03% of total)
prob += 0.02*x_A + 0.04*x_B + 0.03*x_C <= 0.03*(x_A + x_B + x_C), "Phosphorous_Constraint"

# 3. Ash constraint (≤ 3% of total)
prob += 3*x_A + 2*x_B + 5*x_C <= 3*(x_A + x_B + x_C), "Ash_Constraint"

# Solve the problem
prob.solve(PULP_CBC_CMD(msg=0))

# Print the results
print("Status:", LpStatus[prob.status])
print("Maximum Profit (BDT):", value(prob.objective))
print("\nOptimal Solution:")
print("Coal A (tons):", value(x_A))
print("Coal B (tons):", value(x_B))
print("Coal C (tons):", value(x_C))

# Calculate percentages
total = value(x_A) + value(x_B) + value(x_C)
if total > 0:
    print("\nProportions:")
    print("Coal A: {:.1f}%".format(100*value(x_A)/total))
    print("Coal B: {:.1f}%".format(100*value(x_B)/total))
    print("Coal C: {:.1f}%".format(100*value(x_C)/total))

# Verify constraints
if total > 0:
    print("\nActual Impurity Levels:")
    print("Phosphorous: {:.4f}%".format((0.02*value(x_A) + 0.04*value(x_B) + 0.03*value(x_C))/total))
    print("Ash: {:.2f}%".format((3*value(x_A) + 2*value(x_B) + 5*value(x_C))/total))
    