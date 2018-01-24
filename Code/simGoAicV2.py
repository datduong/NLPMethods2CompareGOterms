
import sys, os 
from copy import deepcopy
import numpy as np
import pickle
import re 

def formatOutput (set1,set2,output) : # @output is a 1d tensor, @formatOutputis used only after @input2forward
	nrow = len(set1) ## row is set1 
	ncol = len(set2)
	return output.reshape([nrow,ncol]) # row1 is sentence1 vs every other definitions in the 2nd set 

def readGoUniqueToSpec (path2read):
	go = []
	fin = open(path2read,"r")
	for line in fin: 
		go.append(re.sub(r"\n","",line))
	return (go)

def getSw (term,ic4go):
	if term not in ic4go: 
		# print "need to remove "+term 
		return 0
	ICofTerm = ic4go[term]
	if ICofTerm == 0: 
		return 1
	Kt = 1/ICofTerm
	return ( 1/( 1+ np.exp( -1*Kt ) ) ) 

def getSv (term,ic4go,ancestor4go): 
	# rec = go[term]
	# ancestors = rec.get_all_parents()
	# ancestors = list(ancestors)
	ancestors = deepcopy(ancestor4go [term]) ## hard copy ?? 
	ancestors = ancestors + [term] ## add itself 
	swOfAncestors = [ getSw(x,ic4go=ic4go) for x in ancestors ]
	return ( np.sum ( swOfAncestors ) )

def getCommonParents (term1,term2,ancestor4go): ## ancestors including the inputs 
	set1 = set(ancestor4go[term1]+[term1]) 
	set2 = set(ancestor4go[term2]+[term2]) 
	return list ( set1.intersection(set2) )
	
def sum2Sw (term1,term2,ic4go,ancestor4go): 
	# ancestors = common_parent_go_ids([term1,term2], go) 
	ancestors = getCommonParents(term1,term2,ancestor4go) 
	if len(ancestors) == 0: 
		return 0 ## @len(ancestors) defines if 2 terms are from 2 different ontologies 
		
	# if (len(ancestors) == 1) & ( ('GO:0008150' in ancestors) | ('GO:0003674' in ancestors) | ('GO:0005575' in ancestors) )  : 
		# return -np.inf ## no overlap 
	terms = list(ancestors)
	swsum = [ getSw (x, ic4go=ic4go) for x in terms ]
	return ( 2 * np.sum(swsum) )
	
def aic2goTerms (term1,term2,ic4go,ancestor4go): 
	# term1 = "GO:"+term1
	# term2 = "GO:"+term2
	svA = getSv(term1,ic4go,ancestor4go)
	svB = getSv(term2,ic4go,ancestor4go)
	numerator = sum2Sw(term1,term2,ic4go,ancestor4go)
	# if numerator == -np.inf: ## nothing is shared between 2 go terms, only the root is shared. 
		# return 0 # -np.inf
	return ( numerator/(svA+svB) )
	
def aic1goVs1Sets (go1,g2,ic4go,ancestor4go): ## 
	val = map ( lambda x : aic2goTerms ( x, term2=go1, ic4go=ic4go, ancestor4go=ancestor4go ), g2 ) 
	return (np.max(val)) ## max sim 

def aic2sets (set1,set2,ic4go,ancestor4go): # @aic2goSets compare {a1 a2} vs {b1 b2 b3}, return a vectorized form 
	scoreArr = []
	set1 = ["GO:"+s for s in set1] # had to add back the "GO:" ... really stupid. 
	set2 = ["GO:"+s for s in set2]
	for s1 in set1: 
		for s2 in set2: 
			scoreArr.append( aic2goTerms(s1,s2,ic4go,ancestor4go) ) ## what if it returns NA or inf ?? 
	return scoreArr

def aic2setsArr (set1,set2,ic4go,ancestor4go): # @aic2setsArr compare {a1 a2} vs {b1 b2 b3}, return a matrix form 
	scoreArr = []
	set1 = ["GO:"+s for s in set1] # had to add back the "GO:" ... really stupid. 
	set2 = ["GO:"+s for s in set2]
	for s1 in set1: 
		for s2 in set2: 
			scoreArr.append( aic2goTerms(s1,s2,ic4go,ancestor4go) ) ## what if it returns NA or inf ?? 
	scoreArr = np.array(scoreArr) 
	return formatOutput (set1,set2,scoreArr)
	
def removeGoWithoutIC (g1,ic4go): 
	ret = [] 
	for g in g1: 
		gog = "GO:"+g ## put back the GO: symbol?
		if gog in ic4go: 
			ret.append(gog) 
		# else: 
			# print " rm " + g 
	return ret 
				
def aic2goSets (g1,g2,ic4go,ancestor4go): ## hausdorff 
	## screen out go without ic 
	g1 = removeGoWithoutIC(g1,ic4go) 
	g2 = removeGoWithoutIC(g2,ic4go) 
	val1to2 = np.zeros(len(g1))
	for id,go1 in enumerate(g1): 
		val1to2[id] = aic1goVs1Sets( go1,g2,ic4go,ancestor4go ) 
	#	
	val2to1 = np.zeros(len(g2))
	for id,go2 in enumerate(g2): 
		val2to1[id] = aic1goVs1Sets( go2,g1,ic4go,ancestor4go )
	return ( np.min( [ np.mean(val1to2),np.mean(val2to1) ] ) ) 
	
