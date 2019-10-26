import pandas as pd 
import numpy as np
import string

from nltk.tokenize import sent_tokenize

def sent_tokenizer(text):
    return sent_tokenize(text)

def remove_punctuation(sentence):
    return sentence.translate(str.maketrans('', '', string.punctuation))

def lowercase_text(sentences):
    # lower case all words in sentences 
    for idx,sentence in enumerate(sentences):
        lower_cased_tokens = [word.lower() for word in sentence.split()]
        lower_cased_sentence = " ".join([word for word in lower_cased_tokens])
        sent_without_punct = remove_punctuation(lower_cased_sentence)
        sentences[idx] = sent_without_punct.strip()
    return sentences

def remove_short_sentences(sentences):
    sents = []
    for sentence in sentences:
        if len(sentence.split()) > 2:
            sents.append(sentence)
    return sents

def main():
    with open('finetuning-data/legal.txt') as legal_file:
        legal_data = legal_file.read()
        legal_data = sent_tokenizer(legal_data)
        legal_data = lowercase_text(legal_data)
        legal_data = remove_short_sentences(legal_data)
    with open('finetuning-data/news.txt') as news_file:
        news_data = news_file.read()
        news_data = sent_tokenizer(news_data)
        news_data = lowercase_text(news_data)
    
    legal_df = pd.DataFrame(legal_data, columns=['text'])
    legal_df["label"] = [1]*legal_df.shape[0]
    news_df = pd.DataFrame(news_data, columns=['text'])
    news_df["label"] = [0]*news_df.shape[0]

    print(legal_df.shape)
    print(news_df.shape)

    merged_df = pd.concat([legal_df, news_df])
    merged_df = merged_df.sample(frac=1, random_state=42)
    merged_df['index'] = [i for i in range(merged_df.shape[0])]
    merged_df['alpha'] = ['a']*merged_df.shape[0]
    cols = merged_df.columns.to_list()
    cols = [cols[2],cols[1],cols[0],cols[3]]
    merged_df = merged_df[cols]

    print(merged_df.head(20))
    merged_df.to_csv("tuning-data.tsv",header=False, index=False, sep="\t")

if __name__ == "__main__":
    main()