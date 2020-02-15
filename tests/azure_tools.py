from azure.ai.textanalytics import single_analyze_sentiment, single_extract_key_phrases
from scipy.special import expit
import pickle

key = "24f1f63604d14d16b34aa2849540e6b3"
endpoint = "https://uplyft.cognitiveservices.azure.com/"

# Text Sentiment Analysis using Microsoft Azure
def sentiment_analysis(document, endpoint=endpoint, key=key):
    response = single_analyze_sentiment(endpoint=endpoint, credential=key, input_text=document)
    print("Document Sentiment: {}".format(response.sentiment))
    print("Overall scores: positive={0:.3f}; neutral={1:.3f}; negative={2:.3f} \n".format(
        response.document_scores.positive,
        response.document_scores.neutral,
        response.document_scores.negative,
    ))
    
    return response.document_scores.positive, response.document_scores.neutral, response.document_scores.negative

# Analyze sentiment using Google Cloud tools
def analyze_sentiment_google(text):
    client = language.LanguageServiceClient()
    document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document)
    print(sentiment.document_sentiment.score, sentiment.document_sentiment.magnitude)

# Phrase Extraction
def key_phrase_extraction(document, endpoint=endpoint, key=key):

    try:
        document = document

        response = single_extract_key_phrases(endpoint=endpoint, credential=key, input_text=document)

        if not response.is_error:
            print("Key Phrases:")
            for phrase in response.key_phrases:
                print("\t", phrase)
        else:
            print(response.id, response.error)

    except Exception as err:
        print("Encountered exception. {}".format(err))

f = "cmu_confessions.pickle"
with open(f, 'rb') as conf:
    confs = pickle.load(conf)
    confs = confs[1:]
    for confession in confs[30:40]:
        print(confession)
        pos, neu, neg = sentiment_analysis(confession)
        depIndex = expit((neg - pos) * 4)
        print(depIndex)

        key_phrase_extraction(confession)
        print("\n")