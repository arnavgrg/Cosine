"""
Class to get flesch-kincaid readability score.
"""
from nltk.tokenize import sent_tokenize
import textstat

def get_readability_score_and_grade(text):
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
    paragraphs = text.split("\n\n")
    sentences = []
    for paragraph in paragraphs:
        for sent in sent_tokenize(paragraph):
            sentences.append(sent)
    cleaned_sentences = []
    for sentence in sentences:
        if len(sentence.split()) > 2:
            cleaned_sentences.append(sentence)
    text = " ".join([sentence for sentence in cleaned_sentences])
    print(text)
    score = textstat.flesch_reading_ease(text)
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
    return score, grade