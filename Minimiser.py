from Chisq     import *


class ChiSqIII:
    def __init__(self):
        print 'Create a minimiser'
        startMinimising = Minimiser()

        params     = matrix([0., 1.5]).T
        increments = matrix([0.01, 0.01]).T

        startMinimising.set_StartParams(params, increments)

        print 'Running minimisation'

        blah = ChiSqII()

        while(startMinimising.get_isFinished() != True):
            params = startMinimising.minimise(blah.instance.evaluate())
            blah.instance.setparams(params)

        print startMinimising.get_isFinished(), blah.instance.evaluate()
        print params


class Minimiser:
    def __init__(self):
        self.set_params()

    def set_params(self, params   = [0, 0, 0.00001, 10**6, 0, 10**3, 0, False, 10**11]):
        self.__paramNum           = params[0]
        self.__currentParam       = params[1]
        self.__convLimit          = params[2]
        self.__maxIterations      = params[3]
        self.__currentIterations  = params[4]
        self.__minCycles          = params[5]
        self.__currentCycles      = params[6]
        self.__isFinished         = params[7]
        self.__lastChiSq          = params[8]

        self.__parameters         = matrix([])
        self.__increments         = matrix([])

    def set_StartParams(self, params, incs):
        # Expect params to be a (n,1) matrix (column vector)                                                                 
        self.__paramNum           = params.shape[0]
        self.__parameters         = params
        self.__increments         = incs

    def print_StartParams(self):
        print self.__parameters
        print self.__increments
        print self.__paramNum

    def set_ConvLimit(self, conv):
        self.__convLimit          = conv

    def set_MaxIterations(self, maxIter):
        self.__maxIterations      = maxIter

    def get_isFinished(self):
        return self.__isFinished

    def minimise(self, chisq):
        self.__currentIterations += 1

        if (self.__currentIterations > self.__maxIterations):
            self.__isFinished = True
            print 'Iterations exceeded, finished without convergence'
            return self.__parameters

        if(chisq<self.__lastChiSq and (self.__lastChiSq - chisq) < self.__convLimit):
            # It has converged in this parameter so we move on to the next parameter.                                        
            self.__currentParam += 1

            if(self.__currentParam > (self.__paramNum -1)):
              self.__currentParam   = 0
              self.__currentCycles += 1

              if(self.__currentCycles > self.__minCycles):
                  self.__isFinished = True
                  print 'Minimum cycles exceeded, finished with convergence'
                  return self.__parameters

            self.__parameters[self.__currentParam, 0] += self.__increments[self.__currentParam, 0]

            self.__lastChiSq = chisq

            return self.__parameters

        else:
            # We continue with this parameter                                                                                
            if(chisq < self.__lastChiSq):
                # Continue in the same direction                                                                             
                self.__parameters[self.__currentParam, 0] += self.__increments[self.__currentParam, 0]

                self.__lastChiSq = chisq

                return self.__parameters

            else:
                # Reverse and halve the increment.                                                                           
                self.__increments[self.__currentParam, 0] *= -0.5
                self.__parameters[self.__currentParam, 0] += self.__increments[self.__currentParam, 0]

                self.__lastChiSq = chisq

                return self.__parameters

