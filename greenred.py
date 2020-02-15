from azure.ai.textanalytics import single_analyze_sentiment, single_extract_key_phrases

key = "24f1f63604d14d16b34aa2849540e6b3"
endpoint = "https://uplyft.cognitiveservices.azure.com/"

# Text Sentiment Analysis for one confesstion
def sentiment_analysis(document, endpoint=endpoint, key=key):
    # print("started")
    # print("sending rqs")
    response = single_analyze_sentiment(endpoint=endpoint, credential=key, input_text=document)
    pos, neg = response.document_scores.positive, response.document_scores.negative
    # print("yay")
    return (neg - pos) * 4
        # print("oops")
        # return None

def main(list_documents):
    returnvalue = []
    for i in list_documents:
        value = sentiment_analysis(i)
        if (value >= 0):
            returnvalue.append(True)
        else:
            returnvalue.append(False)
    return returnvalue

