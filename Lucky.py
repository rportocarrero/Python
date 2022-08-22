from random import *

def initialize():
	return [10,10,10,10,10,10,10,10,10,10]

def updateValue(val):
	change = val * .5 if random() < 0.5 else 2
	sign = 1 if random() < 0.5 else -1
	return val + sign * change

def timeStep(list):
	for i in range(len(list)):
		fitness = list[i]
		list[i] = fitness + updateValue(fitness)

population = initialize()

for i in range(100):
	timeStep(population)

print("Max: ",max(population))
print("Min: ",min(population))

