
import sys, os, gensim, requests 
from copy import deepcopy
import numpy as np
import cPickle, pickle, re 

sys.path.append('/u/home/d/datduong/w2vSourceCode/')
from func2cleanASentence4github import * ## clean sentences 
from func2getSimOf2GoTermsV2 import * ## compare 2 go terms 
from SentenceSimilarity import * ## 

def convertDict2Text (Dict,textFullPath): ## --- write dict to a text file 
	keys = Dict.keys()
	numGenes = len(keys)
	f = open(textFullPath,"w")
	for i in range(0,numGenes):
		# write_this = " ".join(j for j in Dict[keys[i]])
		f.write(keys[i] + " " + str(Dict[keys[i]]) + "\n")	
	f.close()	
	
def submitJobs(pairs2test,goAnnotationFile,w2vModel,filefullpath,begin,end):
	
	pairs = [] 
	fin = open (pairs2test,"r")
	for line in fin : ## example FBgn0020616	SA	F18E2.3	scc-3
		line = line.split() 
		if len(line) < 2: 
			continue
		pairs.append ( line ) 
	fin.close() 

	if end > len(pairs): 
		end = len(pairs)
	pairs = pairs[begin:end]
	
	annotationBP = pickle.load(open(goAnnotationFile+"goBP.cPickle","rb"))
	annotationCC = pickle.load(open(goAnnotationFile+"goCC.cPickle","rb"))
	annotationMF = pickle.load(open(goAnnotationFile+"goMF.cPickle","rb"))
	
	model = gensim.models.Word2Vec.load(w2vModel)

	simscore = {}
	counter = 0 
	for pair in pairs: 
	
		gene1 = pair[0]		
		gene2 = pair[1]
		
		ontology = "none"
		try:
			if (pair[0] in annotationBP) & (pair[1] in annotationBP): 
				ontology = "BP"
				score = w2v2GoTerms ( pair[0], pair[1], annotationBP, hausdorffDistMod1to2Wted, model )
			if (pair[0] in annotationCC) & (pair[1] in annotationCC): 
				ontology = "CC"
				score = w2v2GoTerms ( pair[0], pair[1], annotationCC, hausdorffDistMod1to2Wted, model )
			if (pair[0] in annotationMF) & (pair[1] in annotationMF): 
				ontology = "MF"
				score = w2v2GoTerms ( pair[0], pair[1], annotationMF, hausdorffDistMod1to2Wted, model )
		except: 
			print "computation fail ", pair
			continue 
		
		
		simscore [ pair[0] + " " + pair[1] ] = score ##   
		counter = counter + 1
		
	if counter > 0:	## nothing was done, so don't write anything 
		convertDict2Text (simscore,filefullpath)



if len(sys.argv)<1:
	print("Usage: \n")
	sys.exit(1)
else:
	submitJobs ( sys.argv[1], sys.argv[2], sys.argv[3] , sys.argv[4], int(sys.argv[5]), int(sys.argv[6])) 
	
	
	
	




