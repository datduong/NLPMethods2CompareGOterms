simDEF is a method that counts the occurrances of words (very similar to Word2vec). **This is their [paper](https://www.ncbi.nlm.nih.gov/pubmed/26708333).**

**The original [code](https://github.com/ahmadpgh/simDEF)** only compares terms within a single ontology. I modified the simDEF code so that it can compare 2 GO terms from 2 different ontologies. The trick is to 
1. Run step 2 as usual **up until step 2.7** in the original instruction. This step returns 3 matrices **(MF or CC or BP)_Pre_Definition_Matrix.dat**, you can open the files with `vim`. 
2. Merge the 3 matrices **(MF or CC or BP)_Pre_Definition_Matrix.dat** into one single file. You can use command `cat`. Let's say the combined file is Pre_Definition_Matrix_all3.dat.
3. Use the modified code in step 2.8. 
4. I find that simDEF takes a lot of memory because it will create a large 2x2 matrix. It is best to not compare all pairwise comparisons. Here, you can extract only the GO terms you need from the Pre_Definition_Matrix_all3.dat file. Let's say these GO terms are new extracted into a file Pre_Definition_Matrix_all3_small.dat.
5. Pass Pre_Definition_Matrix_all3_small.dat as an input to the last code `step3_getPairWiseScore.R`. 
