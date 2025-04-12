from pulp import *

# Create the problem
prob = LpProblem("Diet_Optimization_BigM", LpMinimize)

# Define the decision variables
x_A = LpVariable("Food_A", 0, None)  # Units of Food A
x_B = LpVariable("Food_B", 0, None)  # Units of Food B

# Big-M value (should be larger than any possible value in the problem)
M = 10000

# Define slack and artificial variables for Big-M method
# For vitamin constraint (≥ 4000)
s1 = LpVariable("Slack_Vitamins", 0, None)
a1 = LpVariable("Artificial_Vitamins", 0, None)

# For mineral constraint (≥ 50)
s2 = LpVariable("Slack_Minerals", 0, None)
a2 = LpVariable("Artificial_Minerals", 0, None)

# For calories constraint (≥ 1400)
s3 = LpVariable("Slack_Calories", 0, None)
a3 = LpVariable("Artificial_Calories", 0, None)

# Define the objective function (minimize cost + M*artificial variables)
prob += 4*x_A + 3*x_B + M*a1 + M*a2 + M*a3, "Total_Cost"

# Add constraints using Big-M method
# Vitamin constraint: 200x_A + 100x_B ≥ 4000
prob += 200*x_A + 100*x_B - s1 + a1 == 4000, "Vitamin_Requirement"

# Mineral constraint: 1x_A + 2x_B ≥ 50
prob += x_A + 2*x_B - s2 + a2 == 50, "Mineral_Requirement"

# Calories constraint: 40x_A + 40x_B ≥ 1400
prob += 40*x_A + 40*x_B - s3 + a3 == 1400, "Calorie_Requirement"

# Solve the problem
prob.solve(PULP_CBC_CMD(msg=0))

# Print the results
print("Status:", LpStatus[prob.status])
print("Minimum Cost (BDT):", value(4*x_A + 3*x_B))  # Actual cost without artificial variables
print("\nOptimal Solution:")
print("Food A (units):", value(x_A))
print("Food B (units):", value(x_B))

# Print nutritional values achieved
#print("\nNutritional Values Achieved:")
#print("Vitamins:", 200*value(x_A) + 100*value(x_B))
#print("Minerals:", value(x_A) + 2*value(x_B))
#print("Calories:", 40*value(x_A) + 40*value(x_B))

# Verify artificial variables are zero (solution is feasible)
#print("\nArtificial Variables (should be zero for feasible solution):")
#print("a1 (Vitamins):", value(a1))
#print("a2 (Minerals):", value(a2))
#print("a3 (Calories):", value(a3))