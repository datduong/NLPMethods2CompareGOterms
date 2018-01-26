These scripts are used to train InferSent model. The code was modified from Wasi to be used for GO database. 

Download the training/testing/development datasets here https://drive.google.com/open?id=1ZC24NJ39rsBTHjE-6WE12OK0WBSOQVnY. 

Train the model by  

```
python3.5 main3.py --bidirection --data /goDataInferSent/ --word_vectors_file w2vModel1Gram11Nov2017NoHeader.txt --word_vectors_directory /goDataInferSent/ --save_path goDataInferSent --cuda --optimizer adam --epochs 15 --batch_size 32
```

This should take about 1-2 hour at most. If you don't have GPU computing, use 

```
python3.5 main3.py --bidirection --data /goDataInferSent/ --word_vectors_file w2vModel1Gram11Nov2017NoHeader.txt --word_vectors_directory /goDataInferSent/ --save_path goDataInferSent --optimizer adam --epochs 15 --batch_size 32
```

The code will run much slower (about 5 hrs for 1 epoch).
