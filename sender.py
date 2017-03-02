import numpy as np
import random
import util

class Sender(object):

	def __init__(self, states, signals, strategy, recordChoices=True, recordStrats=True):
		self.states = states
		self.signals = signals
		self.strategy = strategy
		self._recordChoices = recordChoices
		self._recordStrats = recordStrats
		self._choiceHistory = []
		self._stratHistory = np.array([util.matNormalize(self.strategy)])

	def getSignal(self, state):
		theSig = util.weighted_choice(zip(self.signals, self.strategy[state]))
		#theSig = np.random.choice(self.signals, p=util.normalize(self.strategy[state]))
		if self._recordChoices:
			self._choiceHistory.append((state, theSig))
		return theSig

	def getPaid(self, amount):
		prevChoice = self._choiceHistory[-1]
		#need to test for >0 b/c negative reinforcements
		if self.strategy[prevChoice[0], sum(prevChoice[1])] + amount > 0:
			self.strategy[prevChoice[0], sum(prevChoice[1])] += amount
			if self._recordStrats:
				self.recordStrategy()

	def getNormalizedStrategy(self):
		return util.matNormalize(self.strategy)

	def getChoiceHistory(self):
		return self._choiceHistory

	def getStratHistory(self):
		return self._stratHistory

	def getProb(self, sig, state):
		return self.getNormalizedStrategy()[state, sum(sig)]

        def recordStrategy(self):
		self._stratHistory = np.concatenate((self._stratHistory, [self.getNormalizedStrategy()]))

#NOTE: Decided to change the receiver-type. Demonstrator doesn't really matter
# Think it is just two ways of implementing thr same thing.
# class Demonstrator(Sender):
#
# 	def __init__(self, states, signals, acts, strategy, recordChoices=True, recordStrats=True):
# 		self.states = states
# 		self.signals = signals
# 		self.acts = acts
# 		self.strategy = strategy
# 		self._recordChoices = recordChoices
# 		self._recordStrats = recordStrats
# 		self._choiceHistory = []
# 		self._stratHistory = np.array([util.matNormalize(self.strategy)])
#
# 	def getAction(self, state):
# 		theAct = theState
# 		return theAct
#
# 	def getPaid(self, amount):
# 		prevChoice = self._choiceHistory[-1]
#                 if self.strategy[sum(prevChoice[0]), prevChoice[1]] + amount > 0:
# 		    self.strategy[sum(prevChoice[0]), prevChoice[1]] += amount
# 		if self._recordStrats:
#                     self.recordStrategy()
#
# 	def getProb(self, sig, state):
# 		return self.getNormalizedStrategy()[state, sum(sig)]
