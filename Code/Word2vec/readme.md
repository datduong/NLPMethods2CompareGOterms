
This code was developed in a previous experiment (nearly a year before the newest manuscript). I decided it is best to keep this code on its own. In the case you're interested, please refer to a much the more [detail version](https://github.com/datduong/word2vec2compareGenes). This version was used in early 2017, but the background information remained the same. 

### Download the data sources

This code uses *Anaconda Python 2*. Install python library gensim https://radimrehurek.com/gensim/install.html. 

Download all the scripts in this folder, and also the data in [```DataSource```](https://github.com/datduong/NLPMethods2CompareGOterms/tree/master/DataSource) (if you haven't done so). 

For this code, the Word2vec embedding must be in gensim object format. So download all the files here https://drive.google.com/drive/folders/1E_Y50lSnLDAN4yfPkglf-9aW_hqX8U2g?usp=sharing. Let's say you download these files in a folder name *gensimW2vModel*. 

### Run the main script

Run the main script ```w2vCompareGO.py```. 

The parameters are 

```python w2vCompareGO.py [input file] [GO database path] [w2v model] [output file] [start index] [end index]```. 

The ```[start index] [end index]``` are meant for submitting jobs in parallel. For example, the values ```0 10``` indicate that we will process only line 0 to line 10 in the input file. 

The ```[GO database path]``` is where you download the data in ```DataSource```. 

```[w2v model]``` is the Word2vec embedding (in gensim format). Here you must use the gensim object ```w2vModel1Gram11Nov2017``` that you download from the Google drive. 

To run this example, use 

```python w2vCompareGO.py exampleCases.txt /u/flashscratch/d/datduong/goData/ /u/flashscratch/d/datduong/gensimW2vModel/w2vModel1Gram11Nov2017 output.txt 0 10```

