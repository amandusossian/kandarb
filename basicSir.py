import random
from graphics import *
import matplotlib.pyplot as plt
from statistics import mean


def main(gamma, startBeta, delta, alpha):
    steps = 5
    betaSteps = 1 ## How many Betas? 
    showVis = False #Display Graphics? 
    showSIRPlot = True  # Display final plot over lines?
    #betal = [startBeta + 0.01*i for i in range(betaSteps)] # betalist 
    betal = [startBeta for i in range(steps)]
    rinf = [] # List of different final R-values
    dinf = []
    t0 = [2 + 2*i for i in range(steps)]
    for j in range(steps):
        r,d = runSim(gamma, betal[j],delta, alpha, showVis, showSIRPlot, t0[j])
        rinf.append(r)
        dinf.append(d)
    
    if showSIRPlot and False:
        task2 = []
        for i in range(betaSteps):
            task2.append(betal[i]/gamma)
        plt.scatter(rinf,task2)
        print(mean(rinf))
        plt.show()
    
    plt.plot(t0, rinf)
    plt.show()

def runSim(gamma,beta, delta, alpha, showVis, showSIRPlot, t0):
  
    numAgents = 1000
    gridSize = 100


    if showVis:
        win = GraphWin('Infection Simulation', 400, 400, autoflush = False)
    else: win = 0
    agentList = [agent(win, i,  gamma, beta, delta, alpha, showVis) for i in range(numAgents)]
    Slist = []
    Ilist = []
    Dlist =[]
    Rlist = []
    for agents in agentList:
        if agents.sickState == 0:
            Slist.append(agents)
        else:
            Ilist.append(agents)
    return visuals(Ilist, Slist, Dlist, Rlist, agentList, gridSize, win, showVis, showSIRPlot, t0)
    

def visuals(Ilist, Slist, Dlist, Rlist, agentList, gridSize, win, showVis, showSIRPlot, t0):
    
    t = 0
    hg = gridSize/2 # Half gridsize
    if showVis:
        win.setCoords(-hg-10,-hg-10,hg+10,hg+10)
    s  = [len(Slist)]
    i = [len(Ilist)]
    r = [len(Rlist)]
    tl = [0]
    d = [0]
    while  t<1000 and i[t]>0:
        tl.append(t)
        for agents in agentList:
            agents.update(Ilist, Dlist, Rlist, Slist ,showVis)
        for agents in Ilist:
            agents.infectNebs(Slist, Ilist, showVis)
        s.append(len(Slist))
        i.append(len(Ilist))
        r.append(len(Rlist))
        d.append(len(Dlist))
        #update(30)
        t = t+1
        if t == t0:
            for agents in agentList:
                agents.setD(0.1)
        if t == t0+200:
            agents.setD(1)
        if showSIRPlot:
            if t % 999 == 0 :
                fig = plt.figure()
                ax = fig.add_subplot(1, 1, 1)
                ax.plot(tl, s, color='yellow', label = 'Suceptible')
                ax.plot(tl, r, color='blue', label = 'Recovered')
                ax.plot(tl, i, color = 'red', label = 'Infected')
                ax.plot(tl, d, color = 'black', label = 'Dead')
                s0 = str(t0)
                ax.set_title('Infection plot' + s0+  '= t0')
                ax.legend()
                plt.show()
        if win !=0:
            if win.checkMouse():
                break
                
    
    if showVis:  
        win.getMouse()    
        win.close()
    print(r[t])
    return r[t], d[t]
    
class agent:
    sickState = 0 # S,I,Recov, Dead <=> 0,1,2,3 <=> yellow, red, blue, black 
    xpos, ypos = 0, 0
    temp = 0
    def __init__(self, win, inumber, gamma, beta, delta, alpha, showVis):
        if showVis:
            self.win = win
        self.gamma = gamma
        self.beta = beta
        self.d = 1
        self.delta = delta
        self.alpha = alpha
        
        if inumber % 100 == 0:  # Initiate some sick people
            self.sickState = 1
            self.color = 'red'
        else:
            self.sickState = 0
            self.color = 'yellow'
        self.xpos = random.randint(-49, 49)
        self.ypos = random.randint(-49, 49)
        self.circle = Circle(Point(self.xpos, self.ypos), 1)
        if showVis:
            self.circle.draw(self.win)
            self.circle.setFill(self.color)
       
        
    def setD(self, newD):
        self.d = newD

    def getX(self):
        return self.xpos

    def getY(self):
        return self.ypos

    def setPos(self, incX, incY):
        self.xpos = self.xpos + incX
        self.ypos = self.ypos + incY

    def infectNebs(self, SList, Ilist, showVis):
            neighbours = []
            for agents in SList:
                
                if abs(agents.getX()- self.getX())<=1 and abs(agents.getY()- self.getY())<=1:
                    neighbours.append(agents)
            if random.random()>1-self.beta:
                for neighs in neighbours:
                    neighs.setSick(showVis)
                    neighs.sickState = 1
                    SList.remove(neighs)
                    Ilist.append(neighs)
                
                   
                        
    def move(self,dx,dy, showVis):
        if showVis:
            self.circle.move(dx,dy)
        self.setPos(dx,dy)

    def update(self, Ilist,Dlist, Rlist, Slist, showVis):
        dx,dy = 0,0
        if self.sickState == 1:
            if random.random() > 1-self.delta:
                self.sickState = 3
                if showVis:
                    self.circle.setFill('black')
                Ilist.remove(self)
                Dlist.append(self)
            elif random.random()>1-self.gamma:
                self.sickState = 2
                if showVis:
                    self.circle.setFill('blue')
                Ilist.remove(self)
                Rlist.append(self)
        elif self.sickState == 2:
            if random.random() > 1-self.alpha:
                self.sickState = 0
                if showVis:
                    self.circle.setFill('green')
                Rlist.remove(self)
                Slist.append(self)
        if random.random()>1-self.d and self.sickState != 3:
            moveto = random.randint(1,4)
            if moveto == 1:
                dx,dy = 1,0
            elif moveto == 2:
                dx,dy = 0,1
            elif moveto == 3:
                dx,dy = -1,0
            else: dx,dy = 0,-1
            if (not abs(self.xpos + dx)>49 ) and (not abs(self.ypos + dy)>49): 
                agent.move(self, dx,dy, showVis)
    
    
    def setSick(self, showVis):
        
        if showVis!=0:
            self.color = 'red'
            self.circle.undraw()
            self.circle.draw(self.win)
            self.circle.setFill(self.color)

main(0.01, 0.5, 0, 0) # Probabilities of Recovery, Transmitting the disease, Death, Recovered becoming Susceptible