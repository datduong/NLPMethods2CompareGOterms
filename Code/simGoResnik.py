import sys, os 
from copy import deepcopy
import numpy as np
import pickle
import re 

def formatOutput (set1,set2,output) : # @output is a 1d tensor, @formatOutputis used only after @input2forward
	nrow = len(set1) ## row is set1 
	ncol = len(set2)
	return output.reshape([nrow,ncol]) # row1 is sentence1 vs every other definitions in the 2nd set 

def getCommonParents (term1,term2,ancestor4go): ## ancestors including the inputs 
	set1 = set(ancestor4go[term1]+[term1]) 
	set2 = set(ancestor4go[term2]+[term2]) 
	return list ( set1.intersection(set2) )
	
def maxIC (goArr,ic4go): 
	ic = [] 
	for g in goArr: 
		if g in ic4go: 
			ic.append( ic4go[g] ) 
	return np.max(ic) 
	
def resnik2goTerms (term1,term2,ic4go,ancestor4go): 
	ancestors = getCommonParents(term1,term2,ancestor4go)
	if len(ancestors)==0 : ## no shared ancestors 
		return 0
	return maxIC(ancestors,ic4go)

def resnik1goVs1Sets (go1,goArr2,ic4go,ancestor4go): ## 
	val = [] 
	for go2 in goArr2: 
		val.append( resnik2goTerms(go1,go2,ic4go,ancestor4go) )
	return np.max(val) 

def resnik2sets (set1,set2,ic4go,ancestor4go): # @resnik2sets compare {a1 a2} vs {b1 b2 b3}, return a vectorized form 
	scoreArr = [] # @scoreArr returns an array, so we need to "convert it" into hausdorff distance 
	set1 = ["GO:"+s for s in set1] # had to add back the "GO:" ... really stupid. 
	set2 = ["GO:"+s for s in set2]
	for s1 in set1: 
		for s2 in set2: 
			scoreArr.append( resnik2goTerms(s1,s2,ic4go,ancestor4go) ) ## what if it returns NA or inf ?? 
	return scoreArr 

def resnik2setsArr (set1,set2,ic4go,ancestor4go): # @resnik2sets compare {a1 a2} vs {b1 b2 b3}, return a vectorized form 
	scoreArr = [] # @scoreArr returns an array, so we need to "convert it" into hausdorff distance 
	set1 = ["GO:"+s for s in set1] # had to add back the "GO:" ... really stupid. 
	set2 = ["GO:"+s for s in set2]
	for s1 in set1: 
		for s2 in set2: 
			scoreArr.append( resnik2goTerms(s1,s2,ic4go,ancestor4go) ) ## what if it returns NA or inf ?? 
	scoreArr = np.array(scoreArr) 
	return formatOutput (set1,set2,scoreArr) 
	
