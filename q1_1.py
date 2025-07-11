from pulp import *
import numpy as np
import matplotlib.pyplot as plt

prob=LpProblem('lpp',LpMaximize)

x1=LpVariable("x1",0)
x2=LpVariable("x2",0)


prob += 2*x1+x2,"Obejective"

prob += x1+2*x2<=10,"constraint 1"
prob += x1+x2<=6,"constraint 2"
prob += x1-x2<=2,"constraint 3"
prob += x1-2*x2<=1,"constraint 4"

prob.solve()

print("Status:",LpStatus[prob.status])

for v in prob.variables():
    print (v.name, "=", v.varValue)

print ("The optimal value of the objective function is = ", value(prob.objective))

x=np.arange(0,10)
plt.plot(x,(10-x)/2,label='x1+2x2<=10')
plt.plot(x,6-x,label='x1+x2<=6')
plt.plot(x,x-2,label='x1-x2<=2')
plt.plot(x,(x-1)/2,label='x1-2x2<=1')

plt.axis([-1, 10, -1, 10])
plt.grid(True)
plt.legend()

x = [0,2,4,3,1,0]
y = [5,4,2,1,0,0]
plt.fill(x, y, 'skyblue',alpha=0.5)

plt.text(0.1, 4, 'Feasible \n Region', size = '11')
plt.scatter(x,y,color='blue',s=50)
plt.annotate('Optimal \n solution\n(4,2)', xy = (4,2))
plt.show()