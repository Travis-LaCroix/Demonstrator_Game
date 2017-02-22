# Lewis-Receiver for 2 x 2 Signaling Game in Learning Context
import numpy as np
import random
import util

class Receiver(object):

	def __init__(self, signals, actions, strategy, recordChoices=True, recordStrats=True):
		self.signals = signals
		self.actions = actions
		self.strategy = strategy
		self._recordChoices = recordChoices
		self._recordStrats = recordStrats
		self._choiceHistory = []
		self._stratHistory = np.array([util.matNormalize(self.strategy)])

	def getAction(self, signal):
		raise NotImplementedError

	def getPaid(self, amount):
		raise NotImplementedError

	def getNormalizedStrategy(self):
		return util.matNormalize(self.strategy)

	def getChoiceHistory(self):
		return self._choiceHistory

	def getStratHistory(self):
		return self._stratHistory

	def getProb(self, act, sig):
		raise NotImplementedError

        def recordStrategy(self):
		self._stratHistory = np.concatenate((self._stratHistory, [self.getNormalizedStrategy()]))

class AtomicReceiver(Receiver):

	def getAction(self, signal, state):
		theAct = util.weighted_choice(zip(self.actions, self.strategy[sum(signal)]))
                #np.random.choice requires the weights to be probabilities; is normalizing then using this slower than weighted_choice?
                #theAct = np.random.choice(self.actions, p=util.normalize(self.strategy[sum(signal)]))
		if self._recordChoices:
			self._choiceHistory.append((signal, theAct))
		return theAct

	#Amount is given by thePayoff, from the gameObject file.
	def getPaid(self, amount):
		prevChoice = self._choiceHistory[-1]
                if self.strategy[sum(prevChoice[0]), prevChoice[1]] + amount > 0:
		    self.strategy[sum(prevChoice[0]), prevChoice[1]] += amount
		if self._recordStrats:
                    self.recordStrategy()

	def getProb(self, act, sig):
		return self.getNormalizedStrategy()[sum(sig), act]

class Observer(Receiver):

	def __init__(self, states, signals, actions, strategy, recordChoices=True, recordStrats=True):
		self.states = states
		self.signals = signals
		self.actions = actions
		self.strategy = strategy
		self._recordChoices = recordChoices
		self._recordStrats = recordStrats
		self._choiceHistory = []
		self._stratHistory = np.array([util.matNormalize(self.strategy)])

	def getAction(self, signal, state): #NOTE:This obviously doesn't do what I need it to do.
		theAct = state
		if self._recordChoices:
			self._choiceHistory.append((signal,theAct))
		return theAct

	def getPaid(self, amount):
		prevChoice = self._choiceHistory[-1]
                if self.strategy[sum(prevChoice[0]), prevChoice[1]] + amount > 0:
		    self.strategy[sum(prevChoice[0]), prevChoice[1]] += amount
		if self._recordStrats:
                    self.recordStrategy()

	def getProb(self, act, sig):
		return self.getNormalizedStrategy()[sum(sig), act]

#TODO: CHECK IF THIS IS COMPLETE
