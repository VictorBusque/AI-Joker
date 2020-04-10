import json
import logging
from pprint import pprint
import numpy as np
from tensorflow.keras.models import load_model


class Joker():
    def __init__(self, modelname, mappingname):
        with open(f"Mappings/word2id_{mappingname}.json", "r", encoding="utf8") as f:
            self.word2id = json.load(f)
        self.model = load_model(f"Models/model_{modelname}.h5")
        self.id2word = list(self.word2id.keys())
        self.id2word.sort(key=lambda x: self.word2id[x])

        self.vocabulary_size = len(self.word2id.keys())
        self.sentence_size = 50

    def getData(self, partialString=""):
        partialString = partialString.lower()
        x1 = [ self.word2id[word] if word in self.word2id.keys() else self.word2id["<unk>"] for word in partialString.split() ]
        while len(x1) < self.sentence_size: x1.append(self.word2id["<pad>"])
        x1 = np.array(x1)
        return x1

    def getNextWord(self, sentence):
        nw = len(sentence.split()) #from 0 to nw-1
        x1 = self.getData(sentence)
        preds = self.model.predict( np.array([x1]) )[0] #get predictions for the nwth word
        preds = preds[nw-1] # take next word index from the current word
        argmax = np.argmax(preds)
        prob = preds[argmax]
        answer = self.id2word[argmax]
        if answer == "<unk>": answer = self.id2word[np.argsort(preds)[-2]]
        return answer, prob, argmax

    def getFullJoke(self, sentence):
        while True:
            nextWord,_,_ = self.getNextWord(sentence)
            if nextWord == "<endtoken>": break
            sentence += ' ' + nextWord
            if len(sentence.split())+1 >= self.sentence_size: break
        return sentence

    def getCandidates(self, sentence, ncandidates=5, simTh = 0.7):
        nw = len(sentence.split()) #from 0 to nw-1
        x1 = self.getData(sentence)
        preds = self.model.predict( np.array([x1]) )[0] #get predictions for the nwth word
        preds = preds[nw-1] # take next word index from the current word
        wp = list(zip(self.id2word, preds))
        wp.sort(key=lambda x: x[1] if x[0] not in ["<unk>", "<pad>"] else 0, reverse=True)
        candidates = [(wp[0])]
        refprob = wp[0][1]
        for candidate in wp[1:ncandidates]:
            if candidate[0] in ["<unk>", "<pad>"]: continue
            if candidate[1] >= refprob*simTh: candidates.append(candidate)
        return candidates

    def getInteractiveJoke(self, sentence):
        while True:
            print(f"----------------------------\nWe got: \"{sentence}\"")
            candidates = self.getCandidates(sentence)
            if len(candidates) == 1:
                word = candidates[0][0]
            else:
                print("These are the candidates:")
                for i, candidate in enumerate(candidates):
                    print(f"{i}: {candidate[0]} -> {candidate[1]}")
                opt = input("Choose one: ")
                while int(opt) not in range(len(candidates)): opt = input("Wrong! Choose one: ")
                word = candidates[int(opt)][0]
            if word == "<endtoken>": break
            if len(sentence.split())+1 >= self.sentence_size: break    
            sentence += ' ' + word



if __name__ == "__main__":
    joker = Joker(modelname="JOKE_5", mappingname="JOKE_5")
    while True:
        start = input("> ")
        joker.getInteractiveJoke(start)
        # print(f"Joker says:\n {joker.getFullJoke(start)}")

