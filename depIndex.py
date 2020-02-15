from azure.ai.textanalytics import single_analyze_sentiment, single_extract_key_phrases
from scipy.special import expit
import pickle
import pandas as pd

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
    cnt = 0
    for confession in confList:
        try: 
            total += sentiment_analysis(confession)
            cnt += 1
        except:
            continue

    return total / cnt

if __name__ == "__main__":
    # test on CMU confessions
    """
    fpath = "tests/cmu_confessions.pickle"
    with open(fpath, "rb") as f:
        confessions = pickle.load(f)
        confessions = confessions[1:]
        print(depIndex(confessions))
    """

    # test on all colleges' confessions
    fpath = "../fb-scraper/school_confessions.pickle"
    data = {"School": [], "Index": []}
    with open(fpath, "rb") as f:
        schoolDict = pickle.load(f)
        for school, confessions in schoolDict.items():
            conf_processed = confessions[1:100]
            dep = depIndex(conf_processed)
            print(school + ": " + str(dep))
            data["School"].append(school)
            data["Index"].append(dep)

    df_schools = pd.DataFrame(data)
    print(df_schools)
    df_schools.to_csv("school_indices.csv")