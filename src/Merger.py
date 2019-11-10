"""
.. module:: Merger
    :noindex:
.. moduleauthor:: Filipe Pires [85122] & Joao Alegria [85048]
"""
import io
import os
import math
from abc import ABC, abstractmethod
from decimal import *

getcontext().prec = 2


class Merger(ABC):
    """
    Abstract class and interface for several types of index merging implementations, due to file format or processing method

    :param intermediateIndex: list of the names of the intermedia indexes to be merged into one
    :type intermediateIndex: list<str>
    :param indexer: instance of the indexer used in the context to create the corpus index
    :type indexer: Indexer
    """

    def __init__(self, intermediateIndex, indexer):
        """
        Class constructor
        """
        # self.out = open(filename, "w")
        self.outDir = "index/"
        if not os.path.exists(self.outDir):
            os.makedirs(self.outDir)
        else:
            for f in [f for f in os.listdir("index/")]:
                os.remove("index/"+f)
        self.files = [io.open(x, "r") for x in intermediateIndex]
        self.index = []
        self.indexer = indexer

    @abstractmethod
    def mergeIndex(self):
        """
        Function that merges the intermediate indexes (or blocks of them) into one final index according to our memory-intelligent strategy.
        """
        return True

    @abstractmethod
    def writeIndex(self):
        """
        Function that writes the final index (or blocks of it) to disk according to our memory-intelligent strategy.
        """
        pass

    '''
    def clearVar(self):
        """
        Function that frees the memory currently in use by emptying all class variables.
        """
        pass
    '''


class PositionWeightMerger(Merger):
    def __init__(self, intermediateIndex, indexer):
        """
        Class constructor
        """
        super().__init__(intermediateIndex, indexer)
        self.terms = [x.readline().strip().split(";") for x in self.files]

    def mergeIndex(self):
        """
        Variation of the merge function adapted to the positions and weights format.
        """
        if self.files == []:
            return True
        if "" in self.terms:
            line = self.files[self.terms.index(
                "")].readline().strip().split(";")
            if line == [""]:
                os.remove(self.files[self.terms.index("")].name)
                self.files.remove(self.files[self.terms.index("")])
                self.terms.remove(self.terms[self.terms.index("")])
                return False
            self.terms[self.terms.index("")] = line
            return False

        term = min([x[0][:x[0].find(":")] for x in self.terms])
        docs = []
        for idx, t in enumerate(self.terms):
            if term == t[0][:t[0].find(":")]:
                docs += t[1:]
                self.terms[idx] = ""

        self.index.append((term, {}))
        for d in docs:
            self.index[-1][1][d.split(":")
                              [0]] = d.split(":")[2].split(",")
        docs = []
        return False

    def writeIndex(self):
        """
        Variation of the write function adapted to the positions and weights format.
        """
        # TODO: maybe losing info!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if self.index == []:
            return
        self.index.sort(key=lambda tup: tup[0])
        out = open(self.outDir+self.index[0][0]+"_"+self.index[-1][0], "w")
        auxString = ""
        for t, docs in self.index:
            idf, w2 = self.indexer.normalize(docs)
            auxString += t+":"+str(idf)
            for doc, w in docs.items():
                auxString += ";"+doc+":" + \
                    str(w2[0])+":" + \
                    str(w[0])+"".join(","+str(x) for x in w[1:])
                w2 = w2[1:]
            out.write(auxString+"\n")
            auxString = ""
        self.index = []
        out.close()


class WeightMerger(Merger):
    def __init__(self, intermediateIndex, indexer):
        """
        Class constructor
        """
        super().__init__(intermediateIndex, indexer)
        self.terms = [x.readline().strip().split(";") for x in self.files]

    def mergeIndex(self):
        """
        Variation of the merge function adapted to the weights format.
        """
        if self.files == []:
            return True
        if "" in self.terms:
            line = self.files[self.terms.index(
                "")].readline().strip().split(";")
            if line == [""]:
                os.remove(self.files[self.terms.index("")].name)
                self.files.remove(self.files[self.terms.index("")])
                self.terms.remove(self.terms[self.terms.index("")])
                return False
            self.terms[self.terms.index("")] = line
            return False

        term = min([x[0][:x[0].find(":")] for x in self.terms])
        docs = []
        for idx, t in enumerate(self.terms):
            if term == t[0][:t[0].find(":")]:
                docs += t[1:]
                self.terms[idx] = ""

        self.index.append((term, {}))
        for d in docs:
            self.index[-1][1][d.split(":")[0]] = d.split(":")[1]
        docs = []
        return False

    def writeIndex(self):
        """
        Variation of the write function adapted to the weights format.
        """
        # TODO: maybe losing info!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if self.index == []:
            return
        self.index.sort(key=lambda tup: tup[0])
        out = open(self.outDir+self.index[0][0]+"_"+self.index[-1][0], "w")
        auxString = ""
        for t, docs in self.index:
            idf, w2 = self.indexer.normalize(docs)
            auxString += t+":"+str(idf)
            for doc, w in docs.items():
                auxString += ";"+doc+":" + str(w2[0])
                w2 = w2[1:]
            out.write(auxString+"\n")
            auxString = ""
        self.index = []
        out.close()


class PositionMerger(Merger):
    def __init__(self, intermediateIndex, indexer):
        """
        Class constructor
        """
        super().__init__(intermediateIndex, indexer)
        self.positionIndex = {}
        self.terms = [x.readline().strip().split(";") for x in self.files]

    def mergeIndex(self):
        """
        Variation of the merge function adapted to the positions format.
        """
        if self.files == []:
            return True
        if "" in self.terms:
            line = self.files[self.terms.index(
                "")].readline().strip().split(";")
            if line == [""]:
                os.remove(self.files[self.terms.index("")].name)
                self.files.remove(self.files[self.terms.index("")])
                self.terms.remove(self.terms[self.terms.index("")])
                return False
            self.terms[self.terms.index("")] = line
            return False

        term = min([x[0] for x in self.terms])
        docs = []
        for idx, t in enumerate(self.terms):
            if t[0] == term:
                docs += t[1:]
                self.terms[idx] = ""

        self.index.append((term, {}))
        for d in docs:
            self.index[-1][1][d.split(":")
                              [0]] = d.split(":")[2].split(",")
        docs = []
        return False

    def writeIndex(self):
        """
        Variation of the write function adapted to the positions format.
        """
        # TODO: maybe losing info!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if self.index == []:
            return
        self.index.sort(key=lambda tup: tup[0])
        out = open(self.outDir+self.index[0][0]+"_"+self.index[-1][0], "w")
        auxString = ""
        for t, docs in self.index:
            auxString += t
            for doc, w in docs.items():
                auxString += ";"+doc+":" + \
                    str(len(w))+":" + \
                    str(w[0])+"".join(","+str(x) for x in w[1:])
            out.write(auxString+"\n")
            auxString = ""
        self.index = []
        out.close()


class SimpleMerger(Merger):
    def __init__(self, intermediateIndex, indexer):
        """
        Class constructor
        """
        super().__init__(intermediateIndex, indexer)
        self.terms = [x.readline().strip().split(",") for x in self.files]

    def mergeIndex(self):
        """
        Variation of the merge function adapted to the assignment's 1 format.
        """
        if self.files == []:
            return True
        if "" in self.terms:
            line = self.files[self.terms.index(
                "")].readline().strip().split(",")
            if line == [""]:
                os.remove(self.files[self.terms.index("")].name)
                self.files.remove(self.files[self.terms.index("")])
                self.terms.remove(self.terms[self.terms.index("")])
                return False
            self.terms[self.terms.index("")] = line
            return False

        term = min([x[0] for x in self.terms])
        docs = []
        for idx, t in enumerate(self.terms):
            if t[0] == term:
                docs += t[1:]
                self.terms[idx] = ""

        self.index.append((term, {}))
        for d in docs:
            self.index[-1][1][d.split(":")[0]] = d.split(":")[1]
        docs = []
        return False

    def writeIndex(self):
        """
        Variation of the write function adapted to the assignment's 1 format.
        """
        # TODO: maybe losing info!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if self.index == []:
            return
        self.index.sort(key=lambda tup: tup[0])
        out = open(self.outDir+self.index[0][0]+"_"+self.index[-1][0], "w")
        auxString = ""
        for t, docs in self.index:
            auxString += t
            for doc, w in docs.items():
                auxString += ","+doc+":" + str(w)
            out.write(auxString+"\n")
            auxString = ""
        self.index = []
        out.close()
