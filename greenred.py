from azure.ai.textanalytics import single_analyze_sentiment, single_extract_key_phrases
from colour import Color

key = "24f1f63604d14d16b34aa2849540e6b3"
endpoint = "https://uplyft.cognitiveservices.azure.com/"

# Text Sentiment Analysis for one confesstion
def sentiment_analysis(document, endpoint=endpoint, key=key):
    # print("started")
    # print("sending rqs")
    response = single_analyze_sentiment(endpoint=endpoint, credential=key, input_text=document)
    pos, neg = response.document_scores.positive, response.document_scores.negative
    # print("yay")
    return (pos - neg + 1)/2*31
        # print("oops")
        # return None

def cool(list_documents):
    # gradient = ["FF0000","FF1000","FF2000","FF3000","FF4000","FF5000","FF6000","FF7000","FF8000",
    #             "FF9000",
    #             "FFA000",
    #             "FFB000",
    #             "FFC000",
    #             "FFD000",
    #             "FFE000",
    #             "FFF000",
    #             "FFFF00",
    #             "F0FF00",
    #             "E0FF00",
    #             "D0FF00",
    #             "C0FF00",
    #             "B0FF00",
    #             "A0FF00",
    #             "90FF00",
    #             "80FF00",
    #             "70FF00",
    #             "60FF00",
    #             "50FF00",
    #             "40FF00",
    #             "30FF00",
    #             "20FF00",
    #             "10FF00"]
    gradient = list(Color("#FF6666").range_to(Color("#66FF66"), 32))
    returnvalue = []
    for i in list_documents:
        value = sentiment_analysis(i)
        returnvalue.append(gradient[int(value)].get_web())
    return returnvalue





test = ["hello","good","bad","mouth","fetus"]
print(cool(test))


