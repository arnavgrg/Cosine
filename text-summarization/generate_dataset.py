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

def main():
    with open('finetuning-data/legal.txt') as legal_file:
        legal_data = legal_file.read()
        legal_data = sent_tokenizer(legal_data)
        legal_data = lowercase_text(legal_data)
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
    print(merged_df.head(20))

if __name__ == "__main__":
    main()