import numpy as np
from fractions import Fraction

class continuous:
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
    
class discrete(stochastic):
    #initialize object of discrete stochastic process with transition matrix
    def __init__ (self, transitionMatrix):
        for element in transitionMatrix:
            if round(np.sum(element)) != 1:
                print("Error")
            else:
                self.transitionMatrix = transitionMatrix
                # rows, columns = transitionMatrix.shape
                self.stateSpace = [count for count, element in enumerate(transitionMatrix)]

    
    def makeFraction (self, matrix):
        fractionedArray = []
        for row in matrix:
            i = []
            for probability in row:
                prob = float(probability)
                frac = Fraction(prob).limit_denominator()
                i.append(str(frac))
            fractionedArray.append(i)
        print(np.array(fractionedArray, dtype= object))
        return np.array(fractionedArray, dtype= object)
    
    #n step transition probability, that is n th power of transtion matrix
    def nSteptransition (self , n):
        nSteptransitionMatrix = np.linalg.matrix_power(self.transitionMatrix , n)
        print(nSteptransitionMatrix)
        print("This is matrix of " +str(n)+ "power, and p^(n)(i,j) is the (i,j) term of this transition matrix")

    def stateClassification (self):
        # In order to classify as recurrent or transient we need to raise transition matrix to high power and see if total sum of p(i,i) = inf
        probabilityInInfinity = []
        for i in range(0, len(self.transitionMatrix)):
            prob = self.transitionMatrix[i,i]
            for n in range(2,5000):
                matrix = np.linalg.matrix_power(self.transitionMatrix , n)
                prob = prob + matrix[i,i]
            probabilityInInfinity.append(prob)
        recurrentStates = []
        for count, i in enumerate(probabilityInInfinity):
            if i <=10:
                print("state " +str(count)+" is transcient")
                recurrentStates.append(False)
            else:
                print("state " +str(count)+" is recurrent")
                recurrentStates.append(True)
        self.recurrentStates = recurrentStates
    
    def stationary(self):
        #limit behavior of transition matrix
        nSteptransitionMatrix = np.linalg.matrix_power(self.transitionMatrix , 10000)
        a = self.makeFraction(nSteptransitionMatrix)
        print("each row of above matrix will be stationary distribution")
        self.limitTransitionMatrix = nSteptransitionMatrix
    
    def meanRecurrenceTime (self):
        #here we will use theorem which states that mean recurrence time = 1/pi where pi is limit transition probability of each state
        self.stationary()
        for i in self.stateSpace:
            limitProb = self.limitTransitionMatrix[i,i]
            meanTime = 1/limitProb
            print("mean time of state : " +str(i)+ " is :" +str(meanTime))
    
    def findUsualStaff (self):
        self.stateClassification()
        self.stationary()
        self.meanRecurrenceTime()

    


# a = np.array([
#     [0.4 , 0.6,0],
#     [0.2,0.5,0.3],
#     [0,0.5,0.5]
# ])

# b = np.array([
#      [1/4, 0 , 1/2, 0 , 0, 1/4],
#      [1/6, 1/3 , 1/2 , 0, 0, 0], 
#      [0, 0 ,1/4 , 0 , 3/4, 0],
#      [1/2,  1/6, 1/6, 0, 0, 1/6],
#      [0,0,1/3,0,2/3,0],
#      [0,0,0,0,0,1]
#  ])
# c = np.array([
#      [0.1 , 0.9, 0 , 0],
#      [0.5,0.5 , 0 , 0],
#      [0,0, 0.5, 0.5] ,
#      [0,0,0.5,0.5]
#  ])

# d = np.array([
#     [1/2, 0, 0, 1/2],
#     [0,1/2,1/2,0],
#     [0,1/4,3/4,0],
#     [1/4, 0 , 0, 3/4]
# ])

# s = discrete(b)
# s.findUsualStaff()
