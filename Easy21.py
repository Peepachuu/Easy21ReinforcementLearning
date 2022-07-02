import numpy as np

class Easy21:
    
    def __init__(self, bustLowerBound, bustHigherBound, dealerUpperBound):
        self.bustLowerBound = bustLowerBound
        self.bustHigherBound = bustHigherBound
        self.dealerUpperBound = dealerUpperBound   

    def startGame(self):
        return np.random.randint(1, 11), np.random.randint(1, 11)
        
    def step(self, dealerSum, playerSum, a):
        # 1 is hit 0 is stick
        if a == 1:
            playerSum += self.drawCard()

            if playerSum < self.bustLowerBound or playerSum > self.bustHigherBound:
                reward = -1
                terminate = True 
            else:
                terminate = False
                reward = 0    
        else:
            terminate = True
            while dealerSum < self.dealerUpperBound:
                dealerSum += self.drawCard()

            if dealerSum < self.bustLowerBound or dealerSum > self.bustHigherBound or playerSum > dealerSum:
                reward = 1

            elif playerSum == dealerSum:
                reward = 0

            elif playerSum < dealerSum:
                reward = -1        
               
        return dealerSum, playerSum, reward, terminate      

    def drawCard(self):
        cardColor = 1 if np.random.random() >= 1/3 else -1
        return np.random.randint(1, 11) * cardColor