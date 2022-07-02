import Easy21
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

N0 = 100
qStar = np.zeros((11, 22, 2))
actions = [0, 1]
actionCountFromState = np.zeros((11, 22, 2))
stateVisitCount = lambda dealerSum, playerSum: np.sum(actionCountFromState[dealerSum, playerSum])

def epsilonGreedy(dealerSum, playerSum):
    epsilonT = N0 / (N0 + stateVisitCount(dealerSum, playerSum))
    if np.random.random() < epsilonT:
        action = np.random.randint(0, 2)
    else:
        action = np.argmax([qStar[dealerSum, playerSum, a] for a in actions])
    return action

environment = Easy21.Easy21(1, 21, 17) 
episodes = int(1e6)

for episode in range(episodes):

    terminate = False
    dSum, pSum = environment.startGame()
    statesVisited = []
    totalReward = 0

    while not terminate:
        actionToTake = epsilonGreedy(dSum, pSum)
        actionCountFromState[dSum, pSum, actionToTake] += 1
        statesVisited.append((dSum, pSum, actionToTake)) 
        dSum, pSum, reward, terminate = environment.step(dSum, pSum, actionToTake)
        totalReward += reward

    for (d, p, a) in statesVisited:
        qStar[d, p, a] += (totalReward - qStar[d, p, a]) * (1/actionCountFromState[d, p, a])            

vStar = []
for d in range(1, 11):
    for p in range(1, 22):
        vStar.append([d, p, max(qStar[d, p, 0], qStar[d, p, 1])])

df = pd.DataFrame(vStar, columns=['dealerSum', 'playerSum', 'valueFunction'])

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_trisurf(df['dealerSum'], df['playerSum'], df['valueFunction'], cmap=plt.cm.plasma, linewidth=0, antialiased=True)
plt.show()