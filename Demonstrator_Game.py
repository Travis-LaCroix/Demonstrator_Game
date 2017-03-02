import numpy as np
import itertools as it
import random
import matplotlib.pyplot as plt

from gameObject import Game, NGame, DemoGame

#NUMTRIALS = 10
#NUMITERS = 100
#RECTYPE = 'A'

def writeList(theList, fn):
	thefile = open(fn, 'w')
	for item in theList:
		print>>thefile, item

def runExperiment(gameTypes, reinforcementValues, numtrials, numiters, Nvals, outroot, recordPayoff=200):

	for N in Nvals:

		print 'MOVING TO N =' + str(N)

		for gameType in gameTypes:

			print 'MOVING TO GAMETYPE: ' + gameType

			for i in range(numtrials):

				fulloutroot = outroot+'N'+str(N)+'_'+gameType+'_'+str(reinforcementValues)[1:-1].replace(' ','')+'_trial'+str(i)
				outpay = fulloutroot+'_exppay.txt'
				outsend = fulloutroot+'_sendstrat'
				outrec = fulloutroot+'_recstrat'

				payoffs = np.identity(N)*reinforcementValues[0]
                #   Now, check if the second reinforcementValue is nonzero,
                #   And if so, do something to the payoffs.
                #   When reinforcementValues[1] = 0, for (e.g.) N=2, we get the
                #   Matrix [[1.,0,0],[0,1.,0],[0,0,1.]], which will reinforce
                #   Only the strategies on the diagonal (i.e. coordination).
                #   If (e.g.) reinforcementValues[1]=-1, then we get the matrix
                #   [[1.,-1,-1],[-1,1.,-1],[-1,-1,1.]], which will punish non-diagonal
                #   strategies.
				if reinforcementValues[1] != 0:
					for row in range(len(payoffs)):
						for col in range(len(payoffs[0])):
							if row != col:
								payoffs[row][col] += reinforcementValues[1]

				if gameType == 'atomic':
					game = NGame(N, payoffs)
				elif gameType == 'demo':
					game = DemoGame(N, payoffs)
				else:
					assert False, "Invalid game type specified"

				for j in range(numiters):

					game.onePlay()

					if j % recordPayoff == 0:
						game.recordPayoff()

				print game._payHistory[-1]
				writeList(game._payHistory, outpay)
				np.save(outsend, game.sender._stratHistory[-1])
				np.save(outrec, game.receiver._stratHistory[-1])

#For actual experiment, parameters should be:
#	runExperiment(['atomic','demo'], [1,0], 1000, 10000, [2, 3, 4, 5, 6], 'data/exp_')
runExperiment(['atomic','demo'], [1, 0], 500, 10000, [2,3,4,6,8,10], 'data/exp1_')
#runExperiment(['demo'], [1, 0], 10, 10, [2], 'data/exp2_')
#runExperiment(['atomic','demo'], [1, 0], 10, 10, [2], 'data/exp3_')



"""
for N in [2,3,4,5,6,7]:

	print 'MOVING TO N =' + str(N)

	for RECTYPE in ['F']:

		print 'MOVING TO RECTYPE ' + RECTYPE

		for i in range(NUMTRIALS):

			game = FuncGame(N, RECTYPE)

			OUTROOT='data/exp2_'

			#OUTPAY=OUTROOT+'N'+str(N)+'_rec'+RECTYPE+'_trial'+str(i)+'_exppay.txt'
			#OUTSEND=OUTROOT+'N'+str(N)+'_rec'+RECTYPE+'_trial'+str(i)+'_sendstrat'
			#OUTREC=OUTROOT+'N'+str(N)+'_rec'+RECTYPE+'_trial'+str(i)+'_recstrat'

			OUTPAY=OUTROOT+'N'+str(N)+'_funcgame_constneg_trial'+str(i)+'_exppay.txt'
			OUTSEND=OUTROOT+'N'+str(N)+'_funcgame_constneg_trial'+str(i)+'_sendstrat'
			OUTREC=OUTROOT+'N'+str(N)+'_funcgame_constneg_trial'+str(i)+'_recstrat'
			OUTFUNC=OUTROOT+'N'+str(N)+'_funcgame_constneg_trial'+str(i)+'_recfunc'

			for j in range(NUMITERS):
				game.onePlay()

			writeList(game._payHistory, OUTPAY)
			print game._payHistory[-1]
                        print game.receiver._funcHist[-1]
			#save Sender/Rec strategies in .npy format
			np.save(OUTSEND, game.sender._stratHistory[-1])
			np.save(OUTREC, game.receiver._stratHistory[-1])
                        np.save(OUTFUNC, game.receiver._funcHist)
			#for options about text output,
			#see: http://stackoverflow.com/questions/3685265/how-to-write-a-multidimensional-array-to-a-text-file
			#issue is how to read back in properly
"""
#
#
#
#
# import numpy as np 				#Use for multidimensional arrays
# import itertools as it			#Use for functions creating iterators for efficient looping
# import random					#Generate random number or pick random number from sequence
# import matplotlib.pyplot as plt
#
# from gameObject import Game, NGame, DemoGame
#
# #NUMTRIALS = 10
# #NUMITERS = 100
# #RECTYPE = 'A'
#
# def writeList(theList, fn):
# 	thefile = open(fn, 'w')
# 	for item in theList:
# 		print>>thefile, item
#
# #We need to define the runExperiment method so it actually does something:
# #   We want it to take, for arguments, the game-type, the reinforcement values,
# #   the number of trials and iterations per trial, the dimension of the game,
# #   and an outroot (i.e., a place to save the resultant data).
# def runExperiment(gameTypes, reinforcementValues, numtrials, numiters, Nvals, outroot, recordPayoff=200):
#
# 	#First, we want to know what dimension the game is:
# 	for N in Nvals:
#
# 		print 'MOVING TO N = ' + str(N)
#
#         #We also want to know which gametype we are looking at.
#         #This will be useful when the dimension of the gameTypes array is > 1.
# 		for gameType in gameTypes:
#
# 			print 'MOVING TO GAMETYPE: ' + gameType
#
#             #For each trial, we want to record some data about the game:
# 			for i in range(numtrials):
#
# 				#print 'MOVING TO TRIAL: ' + str(i)
#
#                 #First, we define a full filename to easily read what type of experiment
#                 #   we are looking at
# 				fulloutroot = outroot+'N'+str(N)+'_'+gameType+'_'+str(reinforcementValues)[1:-1].replace(' ','')+'_trial'+str(i)
#                 #The output of this will be something like "data/exp1_N2_atomic_1,0_trial0"
#                 #Now, we want separate files, starting with the info from fulloutroot
#                 #   for each of "Expected Payoff", "Sender Strategy", and "Receiver Strategy"
#                 #   We will save the first as a .txt file, and the other two as .npy files
# 				outpay = fulloutroot+'_exppay.txt'
# 				outsend = fulloutroot+'_sendstrat'
# 				outrec = fulloutroot+'_recstrat'
#
#                 #Now, we want a way of determining what the payoff should be
#                 #We begin by looking at the first element in the reinforcementValues array,
#                 #   and subsequently check if there are any other values (i.e., non-zero).
#                 #   NOTE: np.identity(N) gives an NxN identity matrix.
# 				payoffs = np.identity(N)*reinforcementValues[0]
#                 #   Now, check if the second reinforcementValue is nonzero,
#                 #   And if so, do something to the payoffs.
#                 #   When reinforcementValues[1] = 0, for (e.g.) N=2, we get the
#                 #   Matrix [[1.,0,0],[0,1.,0],[0,0,1.]], which will reinforce
#                 #   Only the strategies on the diagonal (i.e. coordination).
#                 #   If (e.g.) reinforcementValues[1]=-1, then we get the matrix
#                 #   [[1.,-1,-1],[-1,1.,-1],[-1,-1,1.]], which will punish non-diagonal
#                 #   strategies.
# 				if reinforcementValues[1] != 0:
# 					for row in range(len(payoffs)):
# 						for col in range(len(payoffs[0])):
# 							if row != col:
# 								payoffs[row][col] += reinforcementValues[1]
#
#                 #Now, depending on the GameType, we want to instantiate the game
#                 #   from the GAME file (import). A game will take a dimension and
#                 #   Payoffs as arguments.
#                 #If the gameType is 'atomic' we want to instantiate the normal
#                 #   atomic NGame.
# 				if gameType == 'atomic':
# 					game = NGame(N, payoffs)
# 				elif gameType == 'demo':
# 					game = DemoGame(N, payoffs)
# 				else:
# 					assert False, "Invalid game type specified"
#
# 				for j in range(numiters):
#
#                     #See Game file for details on what onePlay does
# 					game.onePlay()
#
#                     #See Game file for details on what recordPayoff does.
# 					if j % recordPayoff == 0:
# 						game.recordPayoff()
#
#                 	#NOTE: [-1] returns the last value in an array.
#                 	#The output of the game, of each run, is the expected payoff
#                 	#   at the end of that run.
# 					print game._payHistory[-1]
# 					writeList(game._payHistory, outpay)
#                 	#Save the sender's strategy at the end of the game to the file,
#                 	#   This will give relative probabilites of picking a signal
#                 	#   given a state.
# 					np.save(outsend, game.sender._stratHistory[-1])
#                 	#Save the receiver's strategy at the end of the game to the file.
# 					np.save(outrec, game.receiver._stratHistory[-1])
#
# #For actual experiment, parameters should be:
# #	runExperiment(['atomic','demo'], [1,0], 1000, 10000, [2, 3, 4, 5, 6], 'data/exp_')
# runExperiment(['atomic'], [1, 0], 10, 10, [2], 'data/exp1_')
# #runExperiment(['demo'], [1, 0], 10, 10, [2], 'data/exp2_')
# #runExperiment(['atomic','demo'], [1, 0], 10, 10, [2], 'data/exp3_')
#
#
#
# """
# for N in [2,3,4,5,6,7]:
#
# 	print 'MOVING TO N =' + str(N)
#
# 	for RECTYPE in ['F']:
#
# 		print 'MOVING TO RECTYPE ' + RECTYPE
#
# 		for i in range(NUMTRIALS):
#
# 			game = FuncGame(N, RECTYPE)
#
# 			OUTROOT='data/exp2_'
#
# 			#OUTPAY=OUTROOT+'N'+str(N)+'_rec'+RECTYPE+'_trial'+str(i)+'_exppay.txt'
# 			#OUTSEND=OUTROOT+'N'+str(N)+'_rec'+RECTYPE+'_trial'+str(i)+'_sendstrat'
# 			#OUTREC=OUTROOT+'N'+str(N)+'_rec'+RECTYPE+'_trial'+str(i)+'_recstrat'
#
# 			OUTPAY=OUTROOT+'N'+str(N)+'_funcgame_constneg_trial'+str(i)+'_exppay.txt'
# 			OUTSEND=OUTROOT+'N'+str(N)+'_funcgame_constneg_trial'+str(i)+'_sendstrat'
# 			OUTREC=OUTROOT+'N'+str(N)+'_funcgame_constneg_trial'+str(i)+'_recstrat'
# 			OUTFUNC=OUTROOT+'N'+str(N)+'_funcgame_constneg_trial'+str(i)+'_recfunc'
#
# 			for j in range(NUMITERS):
# 				game.onePlay()
#
# 			writeList(game._payHistory, OUTPAY)
# 			print game._payHistory[-1]
#                         print game.receiver._funcHist[-1]
# 			#save Sender/Rec strategies in .npy format
# 			np.save(OUTSEND, game.sender._stratHistory[-1])
# 			np.save(OUTREC, game.receiver._stratHistory[-1])
#                         np.save(OUTFUNC, game.receiver._funcHist)
# 			#for options about text output,
# 			#see: http://stackoverflow.com/questions/3685265/how-to-write-a-multidimensional-array-to-a-text-file
# 			#issue is how to read back in properly
# """
