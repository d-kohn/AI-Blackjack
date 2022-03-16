"""
genAlg.py -- Sean Sweeney
A collection of classes to represent the operation of a genetic algorithm
on the n-Queens problem.
"""

from blackjackChrom import chromosome
from random import choices, random
from math import comb
from time import time


"""
Class to hold and gather data about a single population of individual 
chromosomes for use in the genetic algorithm solver
"""
class population(object):

    def __init__(self, pop_num, fit_hands_to_play=10):
        self.num = pop_num
        self.size = 0
        self.list = []
        self.fits = []
        if(fit_hands_to_play):
            self.fit_hands_to_play = fit_hands_to_play
        self.fittest = None
        self.maxFit = 0

    def add(self, new):
        self.list.append(new)
        fitness = new.getFitness(self.fit_hands_to_play)
        self.fits.append(fitness)
        if fitness > self.maxFit:
            self.maxFit = fitness
            self.fittest = new
        self.size += 1

    def getAverageFit(self):
        tot = 0
        for fit in self.fits:
            tot += fit
        return tot/self.size

    def getRandWeighted(self):
        return choices(self.list, self.fits, k=1)[0] #BUG ? - fitnesses are often negative, this raises ValueError


class popNode(object):

    def __init__(self, init_pop):
        self.number = init_pop.num
        self.size = init_pop.size
        self.fittest = init_pop.fittest
        self.maxFit = init_pop.maxFit
        self.avFit = init_pop.getAverageFit()

    def __str__(self):
        ret = ""
        ret += "---------------------------------------\n"
        ret += "popultaion number "+str(self.number)+"\n"
        ret += "population size:    "+str(self.size)+"\n"
        ret += "fittest individual: "+str(self.fittest)+"\n"
        ret += "maximum fitness:    "+str(self.maxFit)+"\n"
        ret += "average fiteness:   "+str(self.avFit)+"\n"
        ret += "---------------------------------------\n"
        return ret



"""
"""
class geneticAlg(object):

    """
    Only parameters are the size of the n-Queens problem to solve and
    the size of each population (kept fixed from generation to generation
    for now)
    """
    def __init__(self, init_popSize, init_mutChance):
        self.popSize = init_popSize
        self.mutChance = init_mutChance


    """
    Generates popSize random n-sized chromosomes and returns a population
    object containing them
    """
    def makeInitialPopulation(self):
        initPop = population(0)
        for _ in range(self.popSize):
            initPop.add(chromosome())
        return initPop


    """
    Takes a list of chromosomes and returns a list of the next generation 
    of chromosomes
    Each chromosome is given a weight - its fitness score
    Then to generate each new chromosome of the next generation two parent
    chromosomes are selected from the parameter population based on weight
    These are crossed over as per the chromosome.crossover() method
    The mutChance parameter is a number 0-1 that represents the likihood 
    that a child chromosome is mutated
    A list containing the next generation of chromosomes is returned
    """
    def getNextPop(self, pop):
        #set up next pop
        nextPop = population(pop.num+1) #Q - why increasing population?
        for _ in range(self.popSize//2):
            p1 = pop.getRandWeighted()
            p2 = pop.getRandWeighted()
            while(p2 == p1):
                p2 = pop.getRandWeighted()
            coPair = p1.crossover(p2)
            child1 = coPair[0]
            child2 = coPair[1]
            if random() < self.mutChance:
                child1.mutate()
            if random() < self.mutChance:
                child2.mutate()
            nextPop.add(child1)
            nextPop.add(child2)
        return nextPop


    """
    Makes numGen number of populations and keeps a list of the fittest 
    individual in each of those populations to return at the end
    """
    def runAlgGenerations(self, numGens, goalFit):
        popNodesList = []
        curPop = self.makeInitialPopulation()
        for _ in range(numGens):
            nextGen = self.getNextPop(curPop)
            if(nextGen.maxFit == goalFit):
                curPop = nextGen
                break
            popNodesList.append(popNode(curPop))
            curPop = nextGen
        popNodesList.append(popNode(curPop))
        return popNodesList

    def runAlgNoImprovement(self, noImproveLength):
        popNodesList = []
        curPop = self.makeInitialPopulation()
        gensNoImprove = 0
        lastAv = 0
        while(True):
            nextGen = self.getNextPop(curPop)
            pn = popNode(curPop)
            curPop = nextGen
            popNodesList.append(pn)
            if pn.avFit <= lastAv:
                gensNoImprove += 1
            else:
                gensNoImprove = 0
                lastAv = pn.avFit
            if gensNoImprove >= noImproveLength:
                break
        popNodesList.append(popNode(curPop))
        return popNodesList

    def runAlgTime(self, timeLimit):
        start = time()
        popNodesList = []
        curPop = self.makeInitialPopulation()
        while(True):
            nextGen = self.getNextPop(curPop)
            popNodesList.append(popNode(curPop))
            curPop = nextGen
            if time()-start >= timeLimit:
                break
        popNodesList.append(popNode(curPop))
        return popNodesList
            

            


        
