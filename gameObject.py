import numpy as np
import random
import util

from sender import Sender
from receiver import *

class Game(object):

	def __init__(self, sender, receiver, states, signals, actions, payoffs=[], stateProbs=[], recordHist=True):
		self.sender = sender
		self.receiver = receiver
		self.states = states
		self.signals = signals
		self.actions = actions
		self.payoffs = payoffs
		#state probabilities; uniform...
		self.stateProbs = util.normalize(np.ones(len(self.states)))
		self._recordHist = recordHist
		self._payHistory = []
		#maxposspay depends on diagonal being max possible
		self._maxPossPay = sum([self.stateProbs[i]*self.payoffs[i, i] for i in self.states])

	def onePlay(self):
		#Start the game by picking a state:
		theState = np.random.choice(self.states, p=self.stateProbs)
		#Go to Sender to pcik a signal for the state
		theSignal = self.sender.getSignal(theState)
		#Go to receiver to pick an act for the signal
		theAct = self.receiver.getAction(theSignal,theState)
		#NOTE: thePayoff takes payoffs, which is the NxN identity matrix, and
		#	Accesses the entry given by theState, and theAct. So, thePayoff == 1
		#	just in case theState == theAct
		thePayoff = self.payoffs[theState, theAct]
		#Send payoff to sender
		self.sender.getPaid(thePayoff)
		#Send payoff
		self.receiver.getPaid(thePayoff)
		if self._recordHist:
			self._payHistory.append(self.getExpectedPayoff())

	def getExpectedPayoff(self):
		theSum = 0.0
		#the below is the fully general calculation
		"""
		for s in self.states:
			for a in self.actions:
				theSum += self.payoffs[s, a] * self.stateProbs[s] * sum([self.sender.getProb(sig, s)*self.receiver.getProb(a, sig) for sig in self.signals])
		"""

		#but, when I'm using the payoffs just to capture negative reinforcement but intuitively
		#still want the identity matrix, here's the hack:
		for s in self.states:
			theSum += sum([self.sender.getProb(sig, s)*self.receiver.getProb(s, sig) for sig in self.signals])

		return theSum / len(self.states)

	def recordPayoff(self):
		self._payHistory.append(self.getExpectedPayoff())

#Create new class for an NGame, which takes a 'Game' object as argument
class NGame(Game):

    #The following instantiates the NGame class
	def __init__(self, N, payoffs=[], rectype='A', stateProbs=[]):
		realN = N
		#realN = 2*N
		states = range(realN)
		actions = range(realN)
		signals = [[i] for i in range(N)]
		#signals = [[i] for i in range(N)] + [[N,i] for i in range(N)]
		if payoffs == []:
			payoffs = np.identity(realN)
		#Uniform sender/receiver strats to start
		self._func = util.derange(list(states))
		sender = Sender(states, signals, np.ones((len(states),len(signals))))
		if rectype=='A':
			receiver = AtomicReceiver(signals, actions, np.ones((len(signals),len(actions))))
		elif rectype=='D':
			receiver = Observer(states, signals, actions, np.ones((len(signals),len(actions))))
		Game.__init__(self, sender, receiver, states, signals, actions, payoffs)

#Create a new class for DemoGame which takes Game as argument
class DemoGame(Game):
	#The following initializes a particular DemoGame
	def __init__(self, N, payoffs=[], rectype='D', stateProbs=[]):
		realN = N
		states = range(realN)
		actions = range(realN)
		signals = [[i] for i in range(N)]
		if payoffs == []:
			payoffs = np.identity(realN)
		#Uniform sender/receiver strats to start
		self._func = util.derange(list(states))
		sender = Sender(states, signals, np.ones((len(states),len(signals))))
		#selector = random.randint(0, 1)
		if rectype=='A':
			receiver = AtomicReceiver(signals, actions, np.ones((len(signals),len(actions))))
		elif rectype=='D':
			receiver = Observer(states, signals, actions, np.ones((len(signals),len(actions))))
		Game.__init__(self, sender, receiver, states, signals, actions, payoffs)

#NOTE: Trying to change "RecType" above doesn't work, since for each run, the game
# is going to be fixed for the number of iterations (i.e., the entire run).
# what is written below used a 50/50 "selector" to pick a receiver, but it only gets
#selected once at the start. We want to (maybe) change the receiver each time.

# class DemoGame(Game):
# 	#The following initializes a particular DemoGame
# 	def __init__(self, N, payoffs=[], rectype='D', stateProbs=[]):
# 		realN = N
# 		states = range(realN)
# 		actions = range(realN)
# 		signals = [[i] for i in range(N)]
# 		if payoffs == []:
# 			payoffs = np.identity(realN) #!!!
# 		#Uniform sender/receiver strats to start
# 		sender = Sender(states, signals, np.ones((len(states),len(signals))))
# 		selector = random.randint(0, 1)
# 		if selector == 0:
#	 		receiver = Observer(states, signals, actions, np.ones((len(signals),len(actions))))
# 		Game.__init__(self, sender, receiver, states, signals, actions, payoffs)

# class DemoGame(Game):
# 	#The following initializes a particular DemoGame
# 	def __init__(self, N, payoffs=[], rectype='D', stateProbs=[]):
# 		realN = N
# 		states = range(realN)
# 		actions = range(realN)
# 		signals = [[i] for i in range(N)]
# 		if payoffs == []:
# 			payoffs = np.identity(realN) #!!!
# 		#Uniform sender/receiver strats to start
# 		self._func = util.derange(list(states))
# 		selector = random.randint(0, 1)
# 		if selector == 0:
# 			sender = Sender(states, signals, np.ones((len(states),len(signals))))
# 		else:
# 			sender = Demonstrator(states, signals, actions, np.ones((len(signals),len(actions))))
# 		receiver = Observer(states, signals, actions, np.ones((len(signals),len(actions))))
# 		Game.__init__(self, sender, receiver, states, signals, actions, payoffs)
