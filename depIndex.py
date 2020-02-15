from azure.ai.textanalytics import single_analyze_sentiment, single_extract_key_phrases
from scipy.special import expit
import pickle
import pandas as pd
#from multiprocessing.dummy import Pool
from tqdm import tqdm
from collections import Counter

key = "24f1f63604d14d16b34aa2849540e6b3"
endpoint = "https://uplyft.cognitiveservices.azure.com/"

# Text Sentiment Analysis for one confesstion
def sentiment_analysis(document, endpoint=endpoint, key=key):
    response = single_analyze_sentiment(endpoint=endpoint, credential=key, input_text=document)
    pos, neg = response.document_scores.positive, response.document_scores.negative
    return (neg - pos) * 4

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


# Providing a depression index over a list of confessions
def depIndex(confList):
    total = 0
    cnt = 0

    key_phrases = Counter()
    # Phrase Extraction
    def key_phrase_extraction(document, endpoint=endpoint, key=key):
        try:
            response = single_extract_key_phrases(endpoint=endpoint, credential=key, input_text=document)
            if not response.is_error:
                for phrase in response.key_phrases:
                    key_phrases[phrase] += 1

        except:
            print("Encountered exception. {}".format(err))

    for confession in chunks(confList, 10):
        try:
            sent = sentiment_analysis('\n'.join(confession))
            total += sent
            cnt += 1
            # if sent > 0:
            key_phrase_extraction('\n'.join(confession))

        except:
            continue

    try: 
        top_phrases = key_phrases.most_common(5)
        top_phrases = list(zip(*top_phrases))
        return expit(total / cnt), top_phrases[0]
    except:
        return None, None

    # results = []
    # p = Pool(1)
    # results = p.map(sentiment_analysis, confList)

    # results = list(filter(lambda x: x is not None, results))

    # return sum(results) / len(results)


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
    phrase_data = {"School": [], "Word": []}
    with open(fpath, "rb") as f:
        schoolDict = pickle.load(f)
        for school, confessions in tqdm(schoolDict.items()):
            conf_processed = confessions[1:100]
            dep, phrases = depIndex(conf_processed)
            print(school + ": " + str(dep))
            print("Top Phrases: ", phrases)
            data["School"].append(school)
            data["Index"].append(dep)

            for phr in phrases:
                phrase_data["School"].append(school)
                phrase_data["Word"].append(phr)

    df_schools = pd.DataFrame(data)
    print(df_schools)
    df_schools.to_csv("school_indices.csv")

    df_phrases = pd.DataFrame(phrase_data)
    print(df_phrases)
    df_phrases.to_csv("top_phrases.csv")