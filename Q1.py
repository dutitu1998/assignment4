import numpy as np
import matplotlib.pyplot as plt
x1 = np.linspace(0, 10, 400)
x2_1 = (10 - x1) / 2
x2_2 = 6 - x1
x2_3 = x1 - 2
x2_4 = (x1 - 1) / 2

plt.figure(figsize=(10, 8))
plt.plot(x1, x2_1, label='x1 + 2x2 <=10')
plt.plot(x1, x2_2, label=r'$x_1 + x_2 \leq 6$')
plt.plot(x1, x2_3, label=r'$x_1 - x_2 \leq 2$')
plt.plot(x1, x2_4, label=r'$x_1 - 2x_2 \leq 1$')

# Add the non-negativity constraints: x1, x2 must be >= 0
plt.axhline(0, color='black', linestyle='--', label=r'$x_2 \geq 0$')
plt.axvline(0, color='black', linestyle='--', label=r'$x_1 \geq 0$')

#  Intersection of Constraint 1 and Constraint 2: x1 + 2x2 = 10,x1 +  x2 = 6
A = np.array([[1, 2], [1, 1]])
b = np.array([10, 6])
intersection_1 = np.linalg.solve(A, b)

#  Intersection of Constraint 2 and Constraint 3: x1 + x2 = 6, x1 - x2 = 2
A = np.array([[1, 1], [1, -1]])
b = np.array([6, 2])
intersection_2 = np.linalg.solve(A, b)

#  Intersection of Constraint 3 and Constraint 4: x1 - x2 = 2, x1 - 2x2 = 1
A = np.array([[1, -1], [1, -2]])
b = np.array([2, 1])
intersection_3 = np.linalg.solve(A, b)

# Intersection of Constraint 4( x1 - 2x2 = 1 )and the x-axis (x2=0)
A = np.array([[1, -2], [1, 0]])
b = np.array([1, 0])
intersection_4 = np.linalg.solve(A, b)

# List the candidate corner points ---
corners = [
    [0, 0],
    [0, min(x2_1[0], x2_2[0], x2_3[0], x2_4[0])],  # Corner on the y-axis given by the smallest value at x1 = 0
    intersection_1,
    intersection_2,
    intersection_3,
    intersection_4
]
# Filter to include only points in the first quadrant (x1, x2 >= 0)
valid_corners = [pt for pt in corners if pt[0] >= 0 and pt[1] >= 0]

# --- Evaluate the objective function, Z = 2x1 + x2, at each valid corner ---
Z_values = [2 * pt[0] + pt[1] for pt in valid_corners]
max_Z = max(Z_values)
optimal_point = valid_corners[Z_values.index(max_Z)]

# Plot the optimal point
plt.scatter(*optimal_point, color='red', s=100, label=f'Optimal Point: ({optimal_point[0]:.2f}, {optimal_point[1]:.2f})')
#cover the feasible region
plt.fill(*zip(*valid_corners), color='lightgray', alpha=0.3, label='Feasible Region')
plt.xlabel(r'$x_1$')
plt.ylabel(r'$x_2$')
plt.title('Graphical Solution of a Linear Programming Problem')
plt.legend()
plt.grid(True)
plt.xlim(0, 7)
plt.ylim(0, 6)
plt.show()
print(f"Optimal Solution: x1 = {optimal_point[0]:.2f}, x2 = {optimal_point[1]:.2f}, Z = {max_Z:.2f}")