import numpy as np 
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt




    
def plotSir():
    temp1 = SH.shape[0]
    temp1 = np.array([i for i in range(temp1)])
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    label1 = 'Susceptible = ' + str(len(SH))
    label2 = 'Recovered = ' + str(len(RH))
    label3 = 'Infected = ' + str(len(IH))
    ax.plot(temp1, SH, color='yellow', label = label1 )
    ax.plot(temp1, RH, color='blue', label = label2 )
    ax.plot(temp1, IH, color = 'red', label = label3 )
    #ax.plot(tl, d, color = 'black', label = 'Dead')
    ax.set_title('Infection plot')
    ax.legend()
    plt.show()

B = 0.8
G = 0.03
D = 0.5


# Parameters of the simulation
n = 10                 # Number of agents 
initial_infected = 5  # Initial infected agents 
N = 100000  # Simulation time
l = 70     # Lattice size

# Historylists used for plotting SIR-graph
IH = np.array([initial_infected-1])
SH = np.array([n-initial_infected+1])
RH = np.array([0])

# Physical parameters of the system 
x = np.floor(np.random.rand(n)*l)          # x coordinates            
y = np.floor(np.random.rand(n)*l)          # y coordinates  
S = np.zeros(n)                            # status array, 0: Susceptiple, 1: Infected, 2: recovered 
Isolated = np.zeros(n)                     # Isolation array, 0: not isolated, 1: Is currently in isolation
toBeIsolated = np.zeros(n)                 # test array; 0: Should not be isolated, 1: Positive test, should be isolated 
Q = np.zeros(n)                            # temperature array
I = np.argsort((x-l/2)**2 + (y-l/2)**2)
S[I[1:initial_infected]] = 1              # Infect agents that are close to center 

nx = x                           # updated x                  
ny = y                           # updated y                  

def setTemps(): 
    for i in np.where(S == 1)[0]:
        Q[i] = 1
def isolate():
    for i in np.where((toBeIsolated== 1))[0]:
        Isolated[i] = 1
t = 0
print(S)
print(Q)
setTemps()
while t<1000 and list(np.where(S==1)[0]):
    
    steps_x_or_y = np.random.rand(n)
    steps_x = steps_x_or_y < D/2
    steps_y = (steps_x_or_y > D/2) & (steps_x_or_y < D)
    for i in np.where(Isolated !=1)[0]:    
        nx[i] = (x[i] + np.sign(np.random.randn()) * steps_x[i]) % l
        ny[i] = (y[i] + np.sign(np.random.randn()) * steps_y[i]) % l
    
    for i in np.where( (Isolated !=1) & (S==1) & ( np.random.rand(n) < B ))[0]:     # loop over infecting agents 
        S[(x==x[i]) & (y==y[i]) & (S==0)] = 1         # Susceptiples together with infecting agent becomes infected 
        
    S[ (S==1) & (np.random.rand(n) < G) ] = 2         # Recovery
    
    # Tests sick agents, if positive test then set in isolation
    for i in np.where( (Q==1) & (np.random.randn(n)<1/2))[0]:
        toBeIsolated[i] = 1
    Isolated = toBeIsolated
    
    x = nx                                              # Update x 
    y = ny                                              # Update y 
    SH = np.append(SH, len(list(np.where(S ==0)[0])))
    IH = np.append(IH, len(list(np.where(S==1)[0])))
    RH = np.append(RH, len(list(np.where(S==2)[0])))
    t+=1
    if t %300 == 0:
        plotSir()

plotSir()