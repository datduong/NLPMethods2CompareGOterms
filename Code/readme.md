The files here compute the similarity score of 2 Gene Ontology (GO) terms.

### Methods to compare 2 GO terms

The 5 methods are [**Resnik**](https://www.jair.org/media/514/live-514-1722-jair.pdf), [**AIC**](https://dl.acm.org/citation.cfm?id=2674838), and **InferSent** metric. The **W2v** metric is in the folder ```Word2vec```. The **simDEF** is in the folder ``simDEF``. **GOssTo** is at the [original source](https://github.com/pwac092/gossto). A lot of thanks to the dev of GOssTo who were very helpful. 

### Download the data sources

To train InferSent model, I used the scripts from [Wasi's github](https://github.com/wasiahmad/universal_sentence_encoder), and modified for applications regarding the Gene Ontology. You will not need to train the model; use the pre-trained model in ```DataSource```. 

Install Anaconda Python 3, and python library pytorch http://pytorch.org/.

Download all the scripts and files in the [```DataSource```](https://github.com/datduong/NLPMethods2CompareGOterms/tree/master/DataSource) into the same folder. 

### Run the main script

Run the main script ```compare2GO.py``` by  

```
python3.5 compare2GO.py --data /u/flashscratch/d/datduong/goData/ --scoreOutput /u/flashscratch/d/datduong/goData/ --nameExpression exampleCasesB2b --pairs2test exampleCases.txt --goAnnotationFile /u/flashscratch/d/datduong/goData/ --pairStartIndex 0 --pairEndIndex 10 --bidirection --save_path /u/flashscratch/d/datduong/goData/ --word_vectors_file w2vModel1Gram11Nov2017NoHeader.txt --word_vectors_directory /u/flashscratch/d/datduong/goData/ --all3 1
```

```/u/flashscratch/d/datduong/goData/``` is where you download the w2v embedding, GO annotation, InferSent data and model. 
This path will not be the same for your computer. Specify the path correctly. 

The options ```--pairStartIndex 0 --pairEndIndex 10``` indicate that you look at line 0 to line 10 in the input file ```exampleCases.txt```. This is meant for submitting parallel jobs, when the input file has too many lines. ```pairEndIndex``` is reset to the number of lines in the input files, if it is too large. 

Add ```--cuda``` option if you have GPU computing. Note, not using GPU will be much slower. For example, use 
```
python3.5 compare2GO.py --cuda --data /u/flashscratch/d/datduong/goData/ --scoreOutput /u/flashscratch/d/datduong/goData/ --nameExpression exampleCasesB2b --pairs2test exampleCases.txt --goAnnotationFile /u/flashscratch/d/datduong/goData/ --pairStartIndex 0 --pairEndIndex 10 --bidirection --save_path /u/flashscratch/d/datduong/goData/ --word_vectors_file w2vModel1Gram11Nov2017NoHeader.txt --word_vectors_directory /u/flashscratch/d/datduong/goData/ --all3 1
```

```--all3 1``` option allows you to combine the 3 ontologies into 3 connected GO trees. Set this to ```--all3 0```, if you want to use the trees separately. 

```exampleCases.txt``` file contains the pairs of GO terms that we want to compare. The pair ```0022900 0009055``` are from 2 different ontologies. Their score only appears if you set ```--all3 1```.

### Output file

This is the **output**, using the option ```--all3 1```

```
0006814 0006874 0.920131 0.00672202 0.107005600925 0.0 BP
0004620 0019905 0.00174957 0.000463715 0.26424381785 0.0 MF
0022900 0009055 0.999945 0.999449 0.719785762065 6.742243 mixed
0016021 0005887 0.999985 0.99999 0.588589011969 2.4929818 CC
0005829 0005615 0.84575 0.101346 0.21246784923 0.0 CC
0005615 0005886 0.983047 0.997896 0.26177632525 0.0 CC
```

The columns are: 
> GO term 1, GO term 2, Prob( term1 entails term2), Prob( term2 entails term1), AIC score, Resnik score, Ontology type. 

*Prob* means *probability*. For learning purposes, we output ```Prob( term1 entails term2), Prob( term2 entails term1)```. **InferSent GO score** is taken as the ```max ( Prob( term1 entails term2), Prob( term2 entails term1) )```. 
