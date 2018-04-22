simDEF is a method that counts the occurrances of words (very similar to Word2vec). **This is their [paper](https://www.ncbi.nlm.nih.gov/pubmed/26708333).**

I modified the simDEF code so that it can compare 2 GO terms from 2 different ontologies. **The original [code](https://github.com/ahmadpgh/simDEF)** only compares terms within a single ontology. 

I find that simDEF takes a lot of memory because it will create a large 2x2 matrix. It is best to not compare all pairwise comparisons. 
