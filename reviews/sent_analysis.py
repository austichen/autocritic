import re
import pickle
import sys
import os
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

cv = pickle.load(open(os.path.join(os.getcwd(),'reviews/cvector.sav'), 'rb'))
model = pickle.load(open(os.path.join(os.getcwd(), 'reviews/sent_analysis_model1.sav'), 'rb'))

REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")

def run(fileName, extraStopWords):
    reviews = []
    for line in open(fileName, 'r', encoding="utf8"):
        reviews.append(line.strip())
    stopwords = set(STOPWORDS)
    stopwords.update(["movie", "film"])
    for stopword in extraStopWords:
        stopwords.add(stopword)
    reviews = preProcessReviews(reviews)
    X = cv.transform(reviews)
    predictions = model.predict(X)

    positiveTally = 0
    total = len(reviews)

    posReviews = []
    negReviews = []
    for index, prediction in enumerate(predictions):
        if prediction == 'positive review':
            positiveTally += 1
            posReviews.append(reviews[index])
        else:
            negReviews.append(reviews[index])

    generateWordCloud(stopwords, posReviews)
    generateWordCloud(stopwords, negReviews, False)
    rating = positiveTally/total
    return rating


def preProcessReviews(reviews):
    reviews = [REPLACE_NO_SPACE.sub("", line.lower()) for line in reviews]
    reviews = [REPLACE_WITH_SPACE.sub(" ", line) for line in reviews]
    return reviews

def generateWordCloud(stopwords, reviews, pos = True):
    filename = os.path.join(os.getcwd(),'reviews/static/reviews/negativeWordCloud.png')
    filenameProd = 'staticfiles/negativeWordCloud.png'
    bgc = "black"
    if pos:
        filename = os.path.join(os.getcwd(),'reviews/static/reviews/positiveWordCloud.png')
        filenameProd = 'staticfiles/positiveWordCloud.png'
        bgc = "white"
    words = " ".join(reviews)
    wordcloud = WordCloud(stopwords=stopwords, background_color=bgc).generate(words)
    wordcloud.to_file(filename)
    wordcloud.to_file(filenameProd)


