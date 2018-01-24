
# from __future__ import print_function
import util2, helper, data, torch, numpy
from classifier import SentenceClassifier
from sklearn.metrics import classification_report
import torch.nn.functional 

import pickle
from score2GOsetsSentEncodeHeader2 import *

from simGoAicV2 import *  
from simGoResnik import *

args = util2.get_args()


def evaluate(model, batches, dictionary):
	"""Evaluate question classifier model on test data."""
	model.eval() # Turn on evaluation mode which disables dropout.
	SCORE = 1
	for batch_no in range(len(batches)):
		test_sentences1, sent_len1, test_sentences2, sent_len2, test_labels = helper.batch_to_tensors(batches[batch_no],dictionary)
		if args.cuda:
			test_sentences1 = test_sentences1.cuda()
			test_sentences2 = test_sentences2.cuda()
			# test_labels = test_labels.cuda()
		##
		softmax_prob = model(test_sentences1, sent_len1, test_sentences2, sent_len2)
		SCORE = torch.nn.functional.softmax(softmax_prob).cpu().data.numpy()[:,0] ##numpy() #.data.numpy() # cpu().tolist()	## use exp(x) / exp(x) + exp(y)
	return np.array(SCORE)

def getScoreSet1Toward2 (set1,set2,model,dictionary,goAnnotation): 
	def1,def2 = getDefinitions(set1,set2,goAnnotation,isJoin=1)
	''' reverse the sentence ordering '''
	arrString = prepareBatchReverse(def1,def2) # ''' reverse the sentence ordering '''
	test_corpus = data.Corpus2(dictionary)
	test_corpus.parse(arrString, args.tokenize)
	test_batches = helper.batchify(test_corpus.data, 2) # args.batch_size=1 
	# print (test_batches)
	# print (test_batches[0])
	score = evaluate(model, test_batches, dictionary) # @score is distance of set 1 toward set 2. distance is not symmetric 
	return score 

ic4goBP = pickle.load(open('HumanICBP.pickle',"rb"))
ic4goCC = pickle.load(open('HumanICCC.pickle',"rb"))
ic4goMF = pickle.load(open('HumanICMF.pickle',"rb"))
ic4goAll3 = pickle.load(open('HumanIC3ontology.pickle',"rb"))
ancestor4goBP = pickle.load(open('GOBPANCESTOR.pickle',"rb")) 
ancestor4goCC = pickle.load(open('GOCCANCESTOR.pickle',"rb"))
ancestor4goMF = pickle.load(open('GOMFANCESTOR.pickle',"rb"))
ancestor4goAll3 = pickle.load(open('GOANCESTORS_full3ont.pickle',"rb"))

if __name__ == "__main__":

	filefullpath = args.scoreOutput + args.nameExpression +str(args.pairStartIndex)+"."+str(args.pairEndIndex)+".txt" # 
	
	print ("loading dictionary/embedding")
	dictionary = helper.load_object(args.save_path + 'gene_dictionary.p')
	embeddings_index = helper.load_word_embeddings(args.word_vectors_directory, args.word_vectors_file, dictionary.word2idx)
	print ("loading model")
	# print (args)
	model = SentenceClassifier(dictionary, embeddings_index, args, select_method='max')
	if args.cuda:
		model = model.cuda()
	helper.load_model_states_from_checkpoint(model, args.save_path + 'model_best.pth.tar', 'state_dict', args.cuda)
	print('vocabulary size = ', len(dictionary))

	annotationBP = pickle.load(open(args.goAnnotationFile+"goBP.cPickle","rb"))
	annotationCC = pickle.load(open(args.goAnnotationFile+"goCC.cPickle","rb"))
	annotationMF = pickle.load(open(args.goAnnotationFile+"goMF.cPickle","rb"))
	annotationAll3 = pickle.load(open(args.goAnnotationFile+"go3ontology.cPickle","rb"))
	
	f = open(args.pairs2test,'r') ## load genes to be tested. [[gene1,gene2],...]
	pairs = []
	for line in f: 
		pairs.append ( line.strip().split() ) 
	#	
	f.close()

	## !! split files 
	if (args.pairStartIndex>len(pairs)): ## @args.pairStartIndex ensures we don't begin at incorrect position 
		# print 'args.pairStartIndex number too high' 
		exit() 
	if (args.pairEndIndex >len(pairs)): 
		args.pairEndIndex = len(pairs)
	# 
	
	print ('args.pairStartIndex ' + str(args.pairStartIndex) + ' args.pairEndIndex ' + str(args.pairEndIndex))
	pairs = pairs[args.pairStartIndex:args.pairEndIndex]; #print (pairs)

	## compare the similarity score 
	simscore = {}
	counter = 0 ## @counter counts number of pairs to compare 
	ontologyType = "none"
	for p in pairs: 
		try: 
			if args.all3 == 0: 
				if (p[0] in annotationBP) and (p[1] in annotationBP): 
					scoreInfersent = getScoreSet1Toward2 ([p[0]],[p[1]],model,dictionary,annotationBP) 
					scoreAic = aic2goTerms ('GO:'+p[0],'GO:'+p[1],ic4goBP,ancestor4goBP)
					scoreResnik = resnik2goTerms ('GO:'+p[0],'GO:'+p[1],ic4goBP,ancestor4goBP)
					ontologyType = "BP"
				elif (p[0] in annotationCC) and (p[1] in annotationCC): 
					scoreInfersent = getScoreSet1Toward2 ([p[0]],[p[1]],model,dictionary,annotationCC) 
					scoreAic = aic2goTerms ('GO:'+p[0],'GO:'+p[1],ic4goCC,ancestor4goCC)
					scoreResnik = resnik2goTerms ('GO:'+p[0],'GO:'+p[1],ic4goCC,ancestor4goCC)
					ontologyType = "CC"
				elif (p[0] in annotationMF) and (p[1] in annotationMF): 
					scoreInfersent = getScoreSet1Toward2 ([p[0]],[p[1]],model,dictionary,annotationMF) 
					scoreAic = aic2goTerms ('GO:'+p[0],'GO:'+p[1],ic4goMF,ancestor4goMF)
					scoreResnik = resnik2goTerms ('GO:'+p[0],'GO:'+p[1],ic4goMF,ancestor4goMF)
					ontologyType = "MF" 
				else: 
					print ("go terms are in different ontologies\n") 
					continue
			if args.all3 == 1:
				else: 
					scoreInfersent = getScoreSet1Toward2 ([p[0]],[p[1]],model,dictionary,annotationAll3) 
					scoreAic = aic2goTerms ('GO:'+p[0],'GO:'+p[1],ic4goAll3,ancestor4goAll3)
					scoreResnik = resnik2goTerms ('GO:'+p[0],'GO:'+p[1],ic4goAll3,ancestor4goAll3)
					ontologyType = "mixed" 
		except: 
			print ('fail case: see go terms') 
			print (p)
			continue
		simscore [ p[0]+" "+p[1] ] = " ".join(str(s) for s in scoreInfersent) + " " + str(scoreAic) + " " + str(scoreResnik) + " " + ontologyType ## keep the alphabet ordering " " + p[4] + " " + p[3]
		counter = counter + 1
		
		
		# if (counter > 0) & (counter % 5000==0) :	## temporarily write to file 
			# print (counter)
			# convertDict2Text (simscore,filefullpath)
			# simscore = {} ## empty out

	##	
	# print (simscore)
	if counter > 0:	## nothing was done, so don't write anything 
		convertDict2Text (simscore,filefullpath)
	## args.pairEndIndex 
	

