These scripts were taken from [Wasi's github](https://github.com/wasiahmad/universal_sentence_encoder), and modified for applications regarding the Gene Ontology. 

Install Anaconda Python 3, and python library pytorch http://pytorch.org/.

Download all the scripts and files in the ```DataSource``` into the same folder. 

Run the main script compare2GO.py by using 

```
python3.5 compare2GO.py --data /u/flashscratch/d/datduong/goData/ --scoreOutput /u/flashscratch/d/datduong/goData/ --nameExpression exampleCasesB2b --pairs2test exampleCases.txt --goAnnotationFile /u/flashscratch/d/datduong/goData/ --pairStartIndex 0 --pairEndIndex 10 --bidirection --save_path /u/flashscratch/d/datduong/goData/ --word_vectors_file w2vModel1Gram11Nov2017NoHeader.txt --word_vectors_directory /u/flashscratch/d/datduong/goData/ --all3 1
```

```/u/flashscratch/d/datduong/goData/``` is where you download the w2v embedding, GO annotation, InferSent data and model. 
This path will not be the same for your computer. Specify the path correctly. 

Add ```--cuda``` option if you have GPU computing. Note, not using GPU will be much slower. For example, use 
```
python3.5 compare2GO.py --cuda --data /u/flashscratch/d/datduong/goData/ --scoreOutput /u/flashscratch/d/datduong/goData/ --nameExpression exampleCasesB2b --pairs2test exampleCases.txt --goAnnotationFile /u/flashscratch/d/datduong/goData/ --pairStartIndex 0 --pairEndIndex 10 --bidirection --save_path /u/flashscratch/d/datduong/goData/ --word_vectors_file w2vModel1Gram11Nov2017NoHeader.txt --word_vectors_directory /u/flashscratch/d/datduong/goData/ --all3 1
```

```--all3 1``` option allows you to combine the 3 ontologies into 3 connected GO trees. Set this to ```--all3 0```, if you want to use the trees separately. 

```exampleCases.txt``` file contains the pairs of GO terms that we want to compare. The pair ```0022900 0009055``` are from 2 different ontologies. Their score only appears if you set ```--all3 1```.
