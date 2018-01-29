To train InferSent model, I used the scripts from [Wasi's github](https://github.com/wasiahmad/universal_sentence_encoder), and modified for applications regarding the Gene Ontology. 

Download the training/testing/development datasets here https://drive.google.com/open?id=1ZC24NJ39rsBTHjE-6WE12OK0WBSOQVnY. Let's say you download them in a folder named *goDataInferSent*. 

Train the model with GPU, using the ```--cuda```. Decrease the ```--batch_size``` if you don't have enough mem on the GPU. 

```
python3.5 main3.py --cuda --bidirection --data goDataInferSent/ --word_vectors_file w2vModel1Gram11Nov2017NoHeader.txt --word_vectors_directory goDataInferSent/ --save_path goDataInferSent/ --optimizer adam --epochs 15 --batch_size 32
```

This should take about 3 hours at most. If you don't have GPU computing, use 

```
python3.5 main3.py --bidirection --data goDataInferSent/ --word_vectors_file w2vModel1Gram11Nov2017NoHeader.txt --word_vectors_directory goDataInferSent/ --save_path goDataInferSent/ --optimizer adam --epochs 15 --batch_size 128
```

The code will run much slower (about 5 hrs for 1 epoch).
