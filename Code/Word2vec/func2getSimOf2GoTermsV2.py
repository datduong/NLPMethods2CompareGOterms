
import sys, os, gensim, cPickle, pickle, re, gzip
import numpy as np

from func2cleanASentence4github import * ## import functions needed to clean setences 
from SentenceSimilarity import * ## import functions needed to compare go terms 


def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
				
def score2sent (sent1,sent2,model): # @score2sent compares how similar are 2 sentences 
	# @sent1 is a sentence type "string"  
	# isinstance(x, types.StringTypes)
	sent1 = " ".join(i for i in sent1) ## because the go definition is split into vector 
	sent2 = " ".join(i for i in sent2) 
	return cosine(model.encode([sent1])[0], model.encode([sent2])[0])

def keepNonEmptyGoTerms (vec1,goAnnot): 
	# vec2 = vec1 
	vec1 = map (removeGO,vec1)
	vec1 = filter( lambda x: x in goAnnot.keys() , vec1 )	## only found in the keys 
	vec1 = filter( lambda x: len(goAnnot[x])>0 , vec1 )
	# if (len(vec1) ==0): 
		# print vec2
	return vec1

def filterGeneDict (GENES,goAnnot2):
	dict2 = {}
	for k in GENES.keys():
		go2keep = keepNonEmptyGoTerms ( GENES[k], goAnnot2 )
		if len ( go2keep ) > 0: ## non empty term 
			dict2[k] = go2keep
	return dict2
	
def formatAGoTerms ( term ) : 
	term = str(term) 
	if "GO" not in term: 
		term = "GO:"+term 
	return (term) 
		
def grepPatternInVec (pattern,array) : 
	return filter(lambda x:re.search(pattern, x), array)
	
def gsesame2GoTerms ( term1, term2, type="AIC" ) : 
	## do a "post" to compare 2 go terms at g-sesame website 
	""" EXAMPLE:::
	import requests
	url = 'http://bioinformatics.clemson.edu/G-SESAME/Program/geneCompareTwo2.php'
	payload = {
			"symbol1": "FAA1",
			"symbol2": "FAA2",
			"isA": "0.8",
			"partOf": "0.6",
			"ontology": "molecular_function",
			"species1": "All",
			"dataSources1[]": "All",
			"evidenceCodes1[]": "All",
			"species2": "All",
			"dataSources2[]": "All",
			"evidenceCodes2[]": "All",
			"submit": "Submit"
	}
	r = requests.post(url, data=payload)
	print r.status_code
	print r.text
	"""
	# term1: 1234567 (without the GO:)
	payload = {
		"tool_id": "2",
		"GOTerm1": "x1",
		"GOTerm2": "x2",
		"method": type, ## "AIC"
		"submit": "Submit"
	}
	url = "http://bioinformatics.clemson.edu/G-SESAME/Program/GOCompareTwo2_AIC.php"
	payload["GOTerm1"]=term1
	payload["GOTerm2"]=term2
	r = requests.post(url, data=payload)
	soup = BeautifulSoup(r.text, 'html.parser')
	similarity = soup.findAll("p") ## similarity
	similarity = map(str,similarity)
	## possible that no results are found for a GO term (due to database not updated) 
	notfound1 = grepPatternInVec ("No result found from GO term GO:"+term1,similarity) # No result found from GO term GO:1904986
	notfound2 = grepPatternInVec ("No result found from GO term GO:"+term2,similarity)
	if (len(notfound1)>0 ) | (len(notfound2)>0 ): ## there is an error message on the page 
		return (-2) 
	#
	similarity = grepPatternInVec ("Semantic similarity of GO terms.*GO:"+term1+".*"+"GO:"+term2,similarity)
	if len(similarity)==0: 
		return (-2) ## fail to find the go terms ? 
	## ... 	
	similarity = removeArrowBrackets(similarity[0]).split() ## similarity can be a vec. by the "grep" 
	"""
	['[', '\\n', 'Semantic', 'similarity', 'of', 'GO', 'terms', 'GO:0045840', 'and', 'GO:1904870', 'is', '0.111', '\\n', ']']
	"""
	similarity = float ( similarity[ similarity.index("is") + 1 ] )
	return (similarity) 
	
def readXMLGOannot(filename="/u/scratch/d/datduong/go_monthly-termdb.rdf-xml"): 
	f = open(filename, 'r')
	GoDefinitions = f.read() ## whole file
	f.close()
	soup = BeautifulSoup(GoDefinitions, 'lxml')
	## get the go id and def. 
	## !!! GO-TERMS / DEF / NAMES ARE IN PROPER ORDER BY DEFAULT. 
	goterms = soup.findAll('go:accession')## go terms id 
	godefinitions = soup.findAll("go:definition") ## definitions 
	gonames = soup.findAll("go:name") ## name of the GO id 	
	## convert go id and def into string
	godefinitions = map(str,godefinitions)
	gonames = map(str,gonames)	
	goterms = map(str,goterms)
	## edit go terms. 
	goterms = map(removeGO,goterms) ## dont want GO:xyz, just need xyz 
	goterms = map(removeArrowBrackets,goterms)
	goterms = stripEleInAVec(goterms)
	try: 
		goterms.remove("all") ## a weird "all" at the last row of goid. 
	except Exception:
		pass 	
	goAnnot = {}
	for iter in range(0,len(goterms)):
		goAnnot[goterms[iter]] = [gonames[iter],godefinitions[iter]] 
	return goAnnot # [goterms,gonames,godefinitions]
	
def getGONameDef (goId1,goAnnot,model,bigram,trigram,toBigram=0,toTrigram=0): 
	# idx1 = goterms.index(goterms[np.random.random_integers(0,numGoTerms-1)]) # index of randomly chosen term 
	# goterms = goAnnot[0]
	# gonames = goAnnot[1]
	# godefinitions = goAnnot[2]
	goData = goAnnot[goId1] # [gonames,godefinitions]
	# idx1 = goAnnot[0].index(goId1) ## LOCATION OF THE GO:ID (WITHOUT THE "GO:")
	# s1 = cleanASentence(removeArrowBrackets(goAnnot[2][idx1]+goAnnot[1][idx1])).strip()
	s1 = goData[0]+" "+goData[1] ## looks like this "a b"
	s1 = re.sub("obsolete"," ",s1)
	s1 = re.sub("OBSOLETE"," ",s1)
	# print s1
	s1 = tokenize1sent(s1) # cleanSentencesInFile(removeArrowBrackets(s1),1,0).strip()
	# print s1 
	# s1 = map(lambda x: x.strip(), s1)	
	# print s1 
	s1 = keepOnlyWordsInModel(s1,model)
	# if toBigram == 1: 
		# s1 = convert2bigram(s1,bigram)
	# if toTrigram == 1: 
		# s1 = convert2trigram(s1,trigram)
	# s1 = keepOnlyWordsInModel2(s1,model)
	# print s1
	return s1 
	
def cleanGOannotXML (goAnnot,model,bigram,trigram,toBigram=0,toTrigram=0):
	## 	PRE-PROCESS THE XML 
	goAnnot2 = {}
	for name in goAnnot.keys():
		sent = getGONameDef (name,goAnnot,model,bigram,trigram,toBigram,toTrigram)
		goAnnot2[name] = sent ## keep "clean" sentences as dictionary
	return goAnnot2

def w2v2GoTerms (goId1,goId2,goAnnot,func2measure,model):
	# REAL GO:ID WITHOUT THE "GO:"
	# func2measure: a function to measure 2 sentences, example: sim2Sentences(s1,s2,model)
	return func2measure(goAnnot[goId1],goAnnot[goId2],model)
	
def gsesame2GoSets (set1,set2,mapping=np.average): 	
	# set1: {Id1,Id2...} ## without the "GO:". MUST BE A STRING.
	set1 = map(removeGO,set1) ## without the "GO:"
	set2 = map(removeGO,set2)
	pairWiseDistance = []
	for s1 in set1: 
		for s2 in set2: 
			pairWiseDistance.append ( gsesame2GoTerms(s1,s2) ) 
	return mapping(pairWiseDistance) # np.average([1,2,3])
	
def formatOutput (set1,set2,output) : # @output is a 1d tensor, @formatOutputis used only after @input2forward
	nrow = len(set1) ## row is set1 
	ncol = len(set2)
	return output.reshape([nrow,ncol]) # row1 is sentence1 vs every other definitions in the 2nd set 

def w2v2GoSetsArr (set1,set2,goAnnot,func2measure,model): 
	pairWiseDistance = []
	for s1 in set1: # @set1: {Id1,Id2...} ## without the "GO:". MUST BE A STRING. 
		for s2 in set2: 
			s1s2 = w2v2GoTerms (s1,s2,goAnnot,func2measure,model)
			s2s1 = w2v2GoTerms (s2,s1,goAnnot,func2measure,model)
			score = (s1s2 + s2s1) / 2.0
			pairWiseDistance.append ( score ) 
	return formatOutput( set1,set2,np.array(pairWiseDistance) )
	
# def w2v2GoSets2 (set1,set2,goAnnot,func2measure,model,mapping=np.average): 
	# # set1: {Id1,Id2...} ## without the "GO:". MUST BE A STRING. 
	# set1 = map(removeGO,set1) ## without the "GO:"
	# set2 = map(removeGO,set2)
	# len1 = len(set1)
	# len2 = len(set2)
	# pairWiseDistance = [] ## row is set 1, col is set 2, in the format 
	# '''
	# x1 y1 y2 y3
	# x2 y1 y2 y3 
	# '''
	# for s1 in set1: 
		# for s2 in set2: 
			# pairWiseDistance.append ( w2v2GoTerms (s1,s2,goAnnot,func2measure,model) ) 
	# ## ... 
	# np2 = np.array(pairWiseDistance) ## convert to array 
	# np2 = np2.reshape((len1,len2))
	# maxOf1All2 = np.max(np2,1) # fix element in set1, what is its max in SET2, find max by going across a row. 
	# maxOf2All1 = np.max(np2,0)
	# return mapping(np.append(maxOf1All2,maxOf2All1)) # np.average([1,2,3])
	
def GenesInPathway (filename): 
	GENES = {} ## DICT keeps all the genes in pathway and their go terms 
	f = open(filename,'r')
	for line in f: 
		line = line.split()
		GO = grepPatternInVec ('GO:',line) ## go terms 
		if len (GO) > 0: 
			gene = line [ line.index(GO[0]) -1 ] # which index is first go term. need this to get the gene name. 
		else: 
			continue 
		if gene not in GENES: 
			GENES[gene] = GO 
	## 
	f.close()
	return GENES
	
def compare1GO2Many (vecGo2,go1,goAnnot,func2measure,model): 
	##!!! IMPORTANT: D(G1,G2) != D(G2,G1) BECAUSE OF HAUSDORFF DISTANCE 
	''' compare one term go1 to a vector vecGo2 
	go1 = '0000002'
	vecGo2 = ['0000002','0000072']
	compare1GO2Many (vecGo2,go1,goAnnot2,hausdorffDistMod1to2Wted,model,bigram,trigram,toTrigram=0)
	'''
	# go1toMany = []
	# for go2 in vecGo2: 
		# go1toMany.append (w2v2GoTerms (go1,go2,goAnnot,func2measure,model,bigram,trigram,toTrigram=0))
	# go1toMany = map (lambda x: w2v2GoTerms(x,goId2=go1,goAnnot=goAnnot,func2measure=func2measure,model=model), vecGo2)
	# print go1toMany
	maxSim = -np.inf
	for go2 in vecGo2: 
		# print go1,go2
		val = w2v2GoTerms(go1,go2,goAnnot,func2measure,model)
		# print val
		if val > maxSim: 
			maxSim = val 
	# print vecGo2,go1,maxSim
	return maxSim
	# return np.max(go1toMany) ## best distance of go1 to ALL vecGo2

def hausdorffDistMod1to2GO (v1,v2): ## v1 is a vect of best_d(1to2) 
	npAv1 = np.average(v1) ## average, mean best(1 vs all in 2) 
	npAv2 = np.average(v2)
	return [ np.min ( [ npAv1, npAv2 ] ), np.mean( [ npAv1, npAv2 ] ) ] ## worst of the 2 (in original hdf, it is worst of the the 2 bests)
	
def w2v2GoSets3 (set1,set2,goAnnot,func2measure,model): 
	# set1: {Id1,Id2...} ## without the "GO:". MUST BE A STRING. 
	# set1 = map(removeGO,set1) ## without the "GO:"
	# set2 = map(removeGO,set2)
	d1toAll2 = np.zeros(len(set1))
	for id,s1 in enumerate(set1):  
		d1toAll2[id] = compare1GO2Many (set2,s1,goAnnot,func2measure,model) 
	## set2
	d2toAll1 = np.zeros(len(set2))	
	for id,s2 in enumerate(set2): 
		d2toAll1[id] = compare1GO2Many (set1,s2,goAnnot,func2measure,model) 
	return hausdorffDistMod1to2GO(d1toAll2,d2toAll1)
	
def gsesameGenesInPathway (GENES,goAnnot): 
	## GENES: a dictionary 
	genes = GENES.keys()
	numGenes = len(genes)
	distance = np.zeros((numGenes,numGenes))
	for i in range(0,numGenes-1):
		print str(i)+" / "+str(numGenes)
		set1 = keepNonEmptyGoTerms ( GENES[ genes[i] ] , goAnnot )
		for j in range(i,numGenes):
			set2 = keepNonEmptyGoTerms ( GENES[ genes[j] ] , goAnnot )
			ij = gsesame2GoSets ( set1 , set2 )
			distance[i,j] = ij
			distance[j,i] = ij 
	return distance
	
def w2v2GenesInPathway (GENES,goAnnot,func2measure,model):
	## GENES: a dictionary 
	GENES = filterGeneDict (GENES,goAnnot) ## FILTER OUT GENES NOT HAVE GOTERMS IN A CATEGORY: MOL_FUNC, CELL_PROC...
	genes = GENES.keys()
	numGenes = len(genes)
	distance = np.zeros((numGenes,numGenes))
	## .. 
	for i in range(0,numGenes-1):
		print genes[i] + " " + str(i)+" / "+str(numGenes)
		# set1 = keepNonEmptyGoTerms ( GENES[ genes[i] ] , goAnnot )
		for j in range(i,numGenes):
			# print genes[j]
			# set2 = keepNonEmptyGoTerms ( GENES[ genes[j] ] , goAnnot )
			ij = w2v2GoSets3 ( GENES[ genes[i] ] , GENES[ genes[j] ] , goAnnot, func2measure, model )
			distance[i,j] = ij
			distance[j,i] = ij 
	return distance ## np array type 

	
