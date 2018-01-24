These scripts were taken from Wasi's github, and modified for applications regarding the Gene Ontology. 

Download all the scripts and the data sources (the .pickle and .cPickle) into the same folder. 

Run the main script compare2GO.py by using 

```
python3.5 compare2GO.py --data /u/flashscratch/d/datduong/goData/ --scoreOutput /u/flashscratch/d/datduong/goData/ --nameExpression exampleCasesB2b --pairs2test exampleCases.txt --goAnnotationFile /u/flashscratch/d/datduong/goData/ --pairStartIndex 0 --pairEndIndex 10 --bidirection --save_path /u/flashscratch/d/datduong/goData/ --word_vectors_file w2vModel1Gram11Nov2017NoHeader.txt --word_vectors_directory /u/flashscratch/d/datduong/w2vModel1Gram11Nov2017/
```

```/u/flashscratch/d/datduong/goData/``` is where InferSent data and model are saved. 
```/u/flashscratch/d/datduong/w2vModel1Gram11Nov2017/``` is the path to the w2v embedding. 

