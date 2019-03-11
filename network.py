import numpy as np
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop


def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)

    return np.argmax(probas)


def get_data(filepath):
    text = open(filepath).read().lower()
    chars = sorted(set(text))

    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))

    return text, chars, char_indices, indices_char


def prepare_sequeces(maxlen, step, text, chars, char_indices):
    sentences = []
    next_chars = []

    for i in range(0, len(text) - maxlen, step):
        sentences.append(text[i: i + maxlen])
        next_chars.append(text[i + maxlen])

    x = np.zeros((len(sentences), maxlen, len(chars)), dtype=bool)
    y = np.zeros((len(sentences), len(chars)), dtype=bool)

    for i, sentence in enumerate(sentences):
        for t, char in enumerate(sentence):
            x[i, t, char_indices[char]] = 1
            y[i, char_indices[next_chars[i]]] = 1

    return sentences, next_chars, x, y


def create_model(maxlen, chars):
    model = Sequential()

    model.add(LSTM(256, input_shape=(maxlen, len(chars))))

    model.add(Dense(len(chars)))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=0.01))

    return model


def generate(model, maxlen, char_indices, indices_char, chars, seed, length, diversity):
    generated = seed

    # pad seed with 0s
    sentence = ('{0:0>' + str(maxlen) + '}').format(seed).lower()

    for i in range(length):
        x_pred = np.zeros((1, maxlen, len(chars)))

        for t, char in enumerate(sentence):
            if char != '0':
                x_pred[0, t, char_indices[char]] = 1

        preds = model.predict(x_pred, verbose=0)[0]
        next_index = sample(preds, temperature=diversity)
        next_char = indices_char[next_index]

        generated += next_char
        sentence = sentence[1:] + next_char

    return generated


def train(model, x, y, epochs, batch_size):
    filepath = "weights-{epoch:02d}-{loss:.4f}.hdf5"

    checkpoint = ModelCheckpoint(
        filepath,
        monitor='loss',
        verbose=0,
        save_best_only=True,
        mode='min'
    )
    callbacks_list = [checkpoint]

    model.fit(x, y, epochs=epochs, batch_size=batch_size, callbacks=callbacks_list)


def train_network(weights=''):
    print("Reading lyrics")
    text, chars, char_indices, indices_char = get_data('data/lyrics.txt')

    # max length of the sequence
    maxlen = 25

    print("Preparing data")
    sentences, next_chars, x, y = prepare_sequeces(maxlen, 1, text, chars, char_indices)

    print("Creating model")
    model = create_model(maxlen, chars)

    # load weights if given
    if weights != '':
        model.load_weights(weights)
        print("Loaded weights {}".format(weights))

    print("Starting training")
    train(model, x, y, 10, 256)


def create_rap(weights, filepath, seed):
    text, chars, char_indices, indices_char = get_data('data/lyrics.txt')

    # max length of the sequence
    maxlen = 25

    # sentences, next_chars, x, y = prepare_sequeces(maxlen, 1, text, chars, char_indices)

    model = create_model(maxlen, chars)

    model.load_weights(weights)

    output = open(filepath, 'w+')

    output.write(generate(model, maxlen, char_indices, indices_char, chars, seed, 2000, 0.3))
