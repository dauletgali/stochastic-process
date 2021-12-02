import numpy as np
from fractions import Fraction

class stochastic:
    transitionMatrix = object()
    generatorMatrix = object()
    
    
    def __init__(self , transitionMatrix = None ,generatorMatrix= None):        
        if generatorMatrix is not None:
            self.generatorMatrix = generatorMatrix
            transmat = np.zeros_like(generatorMatrix, dtype = float)
            count = 0
            while count < len(generatorMatrix):
                for j in range(len(generatorMatrix[count])):
                    parameter = -1 * generatorMatrix[count,count]
                    if j == count:
                        transmat[count,j] = 0
                    else:
                        transmat[count,j] = generatorMatrix[count,j]/parameter
                if np.sum(transmat[count]) == 1:
                    count = count + 1
            self.transitionMatrix = transmat
        
        if transitionMatrix is not None:
            self.transitionMatrix = transitionMatrix
            genMat = np.zeros_like(transitionMatrix, dtype = float)
            count = 0 
            while count < len(transitionMatrix):
                for j in range(len(transitionMatrix[count])):
                    if count != j :
                        rateDecimal = float(transitionMatrix[count,j])
                        rateFraction = Fraction(rateDecimal).limit_denominator()
                        rateInt = rateFraction.denominator
                        genMat[count,j] = rateFraction.numerator
                        genMat[count,count] = -1 * rateInt
                    else:
                        continue
                if np.sum(genMat[count]) == 0:
                    count = count + 1
                else:
                    print('something went wrong')
                    break
            self.generatorMatrix = genMat
            
    
    def makeFraction (self):
        fractionedArray = []
        for row in self.transitionMatrix:
            i = []
            for probability in row:
                prob = float(probability)
                frac = Fraction(prob).limit_denominator()
                i.append(str(frac))
            fractionedArray.append(i)
        print(np.array(fractionedArray, dtype= object))
        return np.array(fractionedArray, dtype= object)
    
    
    #forward and backward equations
    def forwardEquation (self, prob = (int,int)):
        #forward equation definition
        print('Forward equation is in matrix form (P")_t = (P_t)(Q)')
        stateSpace = len(self.generatorMatrix)
        #write down forward equation for p(i,j)
        expression = 'd/(dt) p('+str(prob[0])+','+ str(prob[1])+') = '
        for i in range(1 ,stateSpace):
            a = "p("+str(prob[0])+" , "+str(i)+") * q("+str(i)+" , "+str(prob[1])+") + "
            expression = expression + a
        


        return expression
    
    class discrete:

        def __init__ (self, transitionMatrix):
            for element in transitionMatrix:
                if np.sum(element) != 1:
                    print("Error")
                else:
                    self.transitionMatrix = transitionMatrix
        #multi step transition probability
        @staticmethod
        def changetoFraction (self, arr):
            fractionedArray = []
            for row in arr:
                i = []
                for probability in row:
                    prob = float(probability)
                    frac = Fraction(prob).limit_denominator()
                    i.append(str(frac))
                fractionedArray.append(i)
            print(np.array(fractionedArray, dtype= object))
            return np.array(fractionedArray, dtype= object)


        def findProb (self, m):
            mStepMatrix = np.linalg.matrix_power(self.transitionMatrix, m)
            a = changetoFraction(mStepMatrix)
            print()

        




a = [
    [0.4 , 0.6,0],
    [0.2,0.5,0.3],
    [0.1,0.7,0.2]
]

s = stochastic.discrete(a)
s.findProb(2)
print(s.transitionMatrix)



























# q = np.array([[-2,1,1],[1,-1,0],[2,1,-3]])
# t = np.array([
#     [0, 0.117 , 0.883],
#     [0.432,0,0.568],
#     [0.754, 0.246, 0]
# ])
# print(t)
# sto = stochastic(transitionMatrix=t)
# print(sto.generatorMatrix)
# avb = sto.forwardEquation(prob=(2,2))
# print(avb)








