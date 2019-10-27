import numpy as np
import string 
import time
import json

from bert_serving.client import BertClient
from sklearn.metrics.pairwise import cosine_similarity

import nltk
import networkx as nx
from nltk.tokenize import sent_tokenize
nltk.download('punkt')

with open('sample.json') as text_sample:
    data = json.load(text_sample)

class TextSummarizer(object):
    def __init__(self, payload):
        super().__init__()
        self.payload = payload
        self.sum_length = 10 
        # Split text into sentences 
#        self.sentences = sent_tokenize(self.text) 
 #       self.length = len(self.sentences)
        self.bc = BertClient(ip="52.249.61.86",check_length=False)
        print("Server status:", self.bc.status)

    def get_paragraphs(self):
        text = self.payload["data"]
        self.paragraphs = text.split("\n\n")
        self.sentences = []
        for paragraph in self.paragraphs:
            for sent in sent_tokenize(paragraph):
                self.sentences.append(sent)
        cleaned_sentences = []
        for sentence in self.sentences:
            if len(sentence.split()) > 2:
                cleaned_sentences.append(sentence)
        self.sentences = cleaned_sentences

    def remove_punctuation(self, sentence):
        return sentence.translate(str.maketrans('', '', string.punctuation))

    def lowercase_text(self):
        # lower case all words in sentences 
        for idx,sentence in enumerate(self.sentences):
            lower_cased_tokens = [word.lower() for word in sentence.split()]
            lower_cased_sentence = " ".join([word for word in lower_cased_tokens])
            sent_without_punct = self.remove_punctuation(lower_cased_sentence)
            if sent_without_punct:
                self.sentences[idx] = sent_without_punct.strip()
    
    def get_embeddings(self):
        self.embeddings = self.bc.encode(self.sentences)
        self.length = len(self.sentences)

    def build_similarity_matrix(self):
        self.similarity_matrix = np.zeros([self.length, self.length])
        for i in range(self.length):
            for j in range(self.length):
                if i != j:
                    self.similarity_matrix[i][j] = cosine_similarity([self.embeddings[i]], [self.embeddings[j]])

    def get_important_sentences(self):
        nx_graph = nx.from_numpy_array(self.similarity_matrix)
        print("Running pagerank")
        scores = nx.pagerank(nx_graph)
        ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(self.sentences)), reverse=True)
        return [ranked_sentences[i][1] for i in range(self.sum_length)]

    def get_summary(self):
        '''
        Returns a list of the most important sentences in the legal document.
        '''
        self.get_paragraphs()
        print("Cleaning text input")
        self.lowercase_text()
        print("Generating embeddings")
        self.get_embeddings()
        print("Building similarity matrix")
        self.build_similarity_matrix()
        print("Getting similarity scores")
        summary = self.get_important_sentences()
        print("Top 10 summary points:")
        for sentence in summary: #
            print("> ",sentence) #
        return summary

ts = TextSummarizer(data)
ts.get_summary()
