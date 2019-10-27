"""
Class to get flesch-kincaid readability score.
"""

import textstat

with open('new_sample.txt') as text_sample:
    data = text_sample.read()

class ReadingLevel(object):
    def __init__(self, text):
        self.text = text

    def get_readability_score_and_grade(self):
        """
        Score	Difficulty
        90-100	Very Easy
        80-89	Easy
        70-79	Fairly Easy
        60-69	Standard
        50-59	Fairly Difficult
        30-49	Difficult
        0-29	Very Confusing
        Returns: Score, Grade Level
        """
        score = textstat.flesch_reading_ease(self.text)
        grade = ""
        if score >= 90:
            grade = "Very Easy"
        elif score >= 80: 
            grade = "Easy"
        elif score >= 70:
            grade = "Fairly Easy"
        elif score > 60:
            grade = "Standard"
        elif score > 50:
            grade = "Fairly Difficult"
        elif score > 30:
            grade = "Difficult"
        else:
            grade = "Very Difficult"
        return score,grade

rl = ReadingLevel(data)
score, grade = rl.get_readability_score_and_grade()
print(score, grade)

# from nltk.tokenize import sent_tokenize
# import string

# class ReadingLevel(object):
#     def __init__(self, text):
#         self.text = text
#         self.sentences = sent_tokenize(self.text)
#         self.length = len(self.sentences)

#     def remove_punctuation(self, sentence):
#         return sentence.translate(str.maketrans('', '', string.punctuation))

#     def lowercase_text(self):
#         # lower case all words in sentences 
#         for idx,sentence in enumerate(self.sentences):
#             lower_cased_tokens = [word.lower() for word in sentence.split()]
#             lower_cased_sentence = " ".join([word for word in lower_cased_tokens])
#             sent_without_punct = self.remove_punctuation(lower_cased_sentence)
#             self.sentences[idx] = sent_without_punct.strip()

#     def get_syllable_count(self, word):
#         word = word.lower()
#         count = 0
#         vowels = "aeiouy"
#         if word[0] in vowels:
#             count += 1
#         for index in range(1, len(word)):
#             if word[index] in vowels and word[index - 1] not in vowels:
#                 count += 1
#         if word.endswith("e"):
#             count -= 1
#         if count == 0:
#             count += 1
#         return count

#     def get_avg_word_count_per_sentence(self):
#         num_words = 0
#         for sentence in self.sentences:
#             num_words += len(sentence.split())
#         return num_words/self.length

#     def get_mean_syllable_count_per_word(self):
#         num_words = 0
#         syllable_count = 0
#         for sentence in self.sentences:
#             for word in sentence.split():
#                 num_words += 1
#                 syllable_count += self.get_syllable_count(word)
#         return syllable_count/num_words

#     def fkgl(self, mwcps: float, msylcpw: float) -> float:
#         '''Flesch-Kincaid Grade Level
#         Arguments:
#             mwcps:    mean word count per sentence
#             msylcpw:  mean syllable count per word
#         Returns:
#             float:  The flesch-kincaid grade level
#         '''
#         return (0.39 * mwcps) + (11.8 * msylcpw) - 15.59

#     def get_score(self):
#         self.lowercase_text()
#         print(self.sentences)
#         mean_word_count = self.get_avg_word_count_per_sentence()
#         mean_syllable_count = self.get_mean_syllable_count_per_word()
#         fk_score = self.fkgl(mean_word_count, mean_syllable_count)
#         print(fk_score)

# rl = ReadingLevel(data)
# rl.get_score()