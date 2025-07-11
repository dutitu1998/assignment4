from pulp import *

# Initialize the problem
prob = LpProblem("Diet_Optimization", LpMinimize)

# Define decision variables
x1 = LpVariable("Food_1", lowBound=0, cat='Continuous') #minmum 0 unit i must to buy
x2 = LpVariable("Food_2", lowBound=0, cat='Continuous')
x3 = LpVariable("Food_3", lowBound=0, cat='Continuous')
x4 = LpVariable("Food_4", lowBound=0, cat='Continuous')

# Objective function (minimize cost)
prob += 45 * x1 + 40 * x2 + 85 * x3 + 65 * x4

# Constraints
prob += 3 * x1 + 4 * x2 + 8 * x3 + 6 * x4 >= 800
prob += 2 * x1 + 2 * x2 + 7 * x3 + 5 * x4 >= 200
prob += 6 * x1 + 4 * x2 + 7 * x3 + 4 * x4 >= 700

# Solve the problem with silent mode
prob.solve(PULP_CBC_CMD(msg=0))

# Output result
print(f"Status: {LpStatus[prob.status]}")
print("Optimal Solution:")
print(f"Food 1 (x1): {x1.varValue} units")
print(f"Food 2 (x2): {x2.varValue} units")
print(f"Food 3 (x3): {x3.varValue} units")
print(f"Food 4 (x4): {x4.varValue} units")
print(f"Minimum Cost: {value(prob.objective)} BDT")
