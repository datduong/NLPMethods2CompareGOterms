These scripts were taken from Wasi's github, and modified for applications regarding the Gene Ontology. 

Download all the scripts and the data sources (the .pickle and .cPickle) into the same folder. 

Run the main script compare2GO.py by using 

```
python3.5 compare2GO.py --data /u/flashscratch/d/datduong/goData/ --scoreOutput /u/flashscratch/d/datduong/goData/ --nameExpression exampleCasesB2b --pairs2test exampleCases.txt --goAnnotationFile /u/flashscratch/d/datduong/goData/ --pairStartIndex 0 --pairEndIndex 10 --bidirection --save_path /u/flashscratch/d/datduong/goData/ --word_vectors_file w2vModel1Gram11Nov2017NoHeader.txt --word_vectors_directory /u/flashscratch/d/datduong/w2vModel1Gram11Nov2017/ --all3 1
```

```/u/flashscratch/d/datduong/goData/``` is where InferSent data and model are saved. 
```/u/flashscratch/d/datduong/w2vModel1Gram11Nov2017/``` is the path to the w2v embedding. 
These two paths will not be the same for your computer. Specify these paths correctly. 

```--all3 1``` option allows you to combine the 3 ontologies into 3 connected GO trees. Set this to ```--all3 0```, if you want to use the trees separately. 

```exampleCases.txt``` file contains the pairs of GO terms that we want to compare. The pair ```0022900 0009055``` are from 2 different ontologies. Their score only appears if you set ```--all3 1```.
