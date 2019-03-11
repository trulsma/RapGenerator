# Rap generator

This project allows you to train a neural network to generate rap lyrics.
Lyrics by Eminem and Mac Miller is used

## Requirements

For generating and training
* Python 3.6
* Following packages
    * Tensorflow
    * Keras
    * h5py
   
For gathering data
* Python 3.*
* Following packages
    * beautifulsoup4
    * urllib3

## Training
The network will train on lyrics.txt in the data folder.
To train with starting weights change (for training from scratch leave it empty)
 ```network.train_network('{weights file}')``` in train.py

Run train.py to start training.

E.g.

```python train.py``` 

## Generating
The network will generate lyrics with given weights and seed.
Change the following to generate different outputs.

```network.create_rap('{weights file}', '{output file}', '{seed}')```

Run generate.py to generate lyrics

E.g.

```python generate.py```

## Gathering data
If you want to gather the dataset yourself.
You can change the code if you want different artists.

Run gather_data.py

E.g.

```python gather_data.py```

 
