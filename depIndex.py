from azure.ai.textanalytics import single_analyze_sentiment, single_extract_key_phrases
from scipy.special import expit
import pickle

key = "24f1f63604d14d16b34aa2849540e6b3"
endpoint = "https://uplyft.cognitiveservices.azure.com/"

# Text Sentiment Analysis for one confesstion
def sentiment_analysis(document, endpoint=endpoint, key=key):
    response = single_analyze_sentiment(endpoint=endpoint, credential=key, input_text=document)
    pos, neg = response.document_scores.positive, response.document_scores.negative
    return expit((neg - pos) * 4)

# Providing a depression index over a list of confessions
def depIndex(confList):
    total = 0
    for confession in confList:
        total += sentiment_analysis(confession)

    return total / len(confList)

if __name__ == "__main__":
    # test on CMU confessions
    fpath = "tests/cmu_confessions.pickle"
    with open(fpath, "rb") as f:
        confessions = pickle.load(f)
        confessions = confessions[1:]
        print(depIndex(confessions))