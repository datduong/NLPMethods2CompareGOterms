
This code was developed in a previous experiment (nearly a year before the newest manuscript). I decided it is best to keep this code on its own. 

This code uses *Anaconda Python 2*. Install python library gensim https://radimrehurek.com/gensim/install.html. 

Download all the scripts in this folder, and also the data in ```DataSource``` (if you haven't done so). 

Run the main script ```w2vCompareGO.py```. 

The parameters are 

```python w2vCompareGO.py [input file] [GO database path] [w2v model] [output file] [start index] [end index]```. 

The ```[start index] [end index]``` are meant for submitting jobs in parallel. For example, the values ```0 10``` indicate that we will process only line 0 to line 10 in the input file. 
