
## compare 2 sets of gene ontology definitions 

import sys,re,os,pickle
import numpy as np  



def convertDict2Text (Dict,textFullPath): ## --- write dict to a text file 
	# numGenes = len(Dict.keys())
	if os.path.exists(textFullPath): 
		print ("warning, output path exists, results will be appended.\n")
		f = open(textFullPath,"a")
	else: 
		f = open(textFullPath,"w")
	for k in Dict.keys():
		# write_this = " ".join(j for j in Dict[keys[i]])
		f.write(k + " " + str(Dict[k]) + "\n")	
	f.close()	

def getDefinitions (set1,set2,goAnnotation,isJoin=0):
	if isJoin == 1: ## joint the words so because @build_vocab use .split() on the sentence 
		def1 = [ " ".join( k for k in goAnnotation[i] ) for i in set1 ] ## @goAnnotation contains definitions already split into words 
		def2 = [ " ".join( k for k in goAnnotation[i] ) for i in set2 ]
	else: 
		def1 = [ goAnnotation[i] for i in set1 ] 
		def2 = [ goAnnotation[i] for i in set2 ]
	return def1, def2 
	
def prepareBatch (def1,def2): ## @prepareBatch creates array like [['a','b'], [...] ]
	# @def1,def2 must be split into words 
	batch = []
	for d1 in def1: ## make every possible pairs 
		for d2 in def2: 
			batch.append([d1,d2]) 
	## 
	return batch
	
def prepareBatchReverse (def1,def2): ## @prepareBatch creates array like [['a','b'], [...] ]
	# @def1,def2 must be split into words 
	batch = []
	for d1 in def1: ## make every possible pairs 
		for d2 in def2: 
			batch.append([d1,d2]) 
			batch.append([d2,d1]) 
	## 
	return batch
	
def formatOutput (set1,set2,output) : # @output is a 1d tensor, @formatOutputis used only after @input2forward
	nrow = len(set1) ## row is set1 
	ncol = len(set2)
	return output.reshape([nrow,ncol]) # row1 is sentence1 vs every other definitions in the 2nd set 

def scoreMhd (set1,set2,output): # @output is a matrix . 
	output = formatOutput (set1,set2,output) 
	rowMax = np.amax(output,1) ## max for each row
	# print (rowMax)
	rowMean = np.mean(rowMax)
	# print (rowMean)
	# colMax = np.amax(output,0) ## max for each col !! WORKS ONLY IF THE METRIC IS SYMMETRIC FOR TERM1 VS TERM2 
	# colMean = np.mean(colMax)
	# return ( np.min([rowMean,colMean]) ) # hausdorff distance 
	return rowMean
	
def scoreMhdSym (set1,set2,output): # @output is a vector, it will be converted into matrix  .
	if type(output) is not np.ndarray:
		output = np.array(output) 
	#
	output = formatOutput (set1,set2,output) 
	rowMax = np.amax(output,1) ## max for each row
	# print (rowMax)
	rowMean = np.mean(rowMax)
	# print (rowMean)
	colMax = np.amax(output,0) ## max for each col !! WORKS ONLY IF THE METRIC IS SYMMETRIC FOR TERM1 VS TERM2 
	colMean = np.mean(colMax)
	return np.min([rowMean,colMean]) , np.mean([rowMean,colMean])  # hausdorff distance 

def scoreMhdSym0 (set1,set2,output): # @output is a matrix .
	output = formatOutput (set1,set2,output) 
	rowMax = np.amax(output,1) ## max for each row
	# print (rowMax)
	rowMean = np.mean(rowMax)
	# print (rowMean)
	colMax = np.amax(output,0) ## max for each col !! WORKS ONLY IF THE METRIC IS SYMMETRIC FOR TERM1 VS TERM2 
	colMean = np.mean(colMax)
	return rowMean,colMean # hausdorff distance 
