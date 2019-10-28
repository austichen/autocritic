from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import json
import re
from bs4 import BeautifulSoup
from . import sent_analysis
import os

GOOGLE_API_KEY=os.environ['GOOGLE_API_KEY']


def index(request):
    return render(request, 'reviews/index.html')
# Create your views here.

def movie(request):
    if request.method == 'GET':
        movieTitle = request.GET.get('title')
        if not movieTitle:
            response = JsonResponse({'message': 'Invalid request: title query invalid'}, status = 400)
            return response
        
        link = None
        res = requests.get('https://www.googleapis.com/customsearch/v1?q='+movieTitle+'&cx=008963822358995440322:m2xfglpsusn&key='+GOOGLE_API_KEY)
        res_json = json.loads(res.text)
        search_result_items = res_json['items']
        for result in search_result_items:
            pageLink = result['link']
            if re.match(r'https://www\.rottentomatoes\.com/m/([^/]*)$', pageLink):
                link = pageLink + '/reviews'
                break
        if link is None:
            response = JsonResponse({'message': 'Internal server error: Unable to find movie'}, status = 500)
            return response
        res = requests.get(link)
        rtHtml = BeautifulSoup(res.text, 'html.parser')
        res = requests.get(link.replace('/reviews', ''))
        rtHomeHtml = BeautifulSoup(res.text, 'html.parser')
        totalPages = int(rtHtml.select('span.pageInfo')[0].text.split(' ').pop())
        imageUrl = rtHtml.select('.panel-body.content_body img')[0]['src']
        movieTitle = rtHtml.select('.panel-body.content_body h2 > a')[0].text
        reviews = rtHtml.select('.review_table .the_review')
        tomatometerScore = int(re.sub(r'[^0-9]', '', rtHomeHtml.select('h2.mop-ratings-wrap__score span.mop-ratings-wrap__percentage')[0].text))

        reviewList = []

        for review in reviews:
            if len(review.text) > 2:
                reviewList.append(review.text)

        for i in range(2, totalPages+1):
            res = requests.get(link + '?page=' + str(i))
            pageHtml = BeautifulSoup(res.text, 'html.parser')
            reviews = pageHtml.select('#reviews .the_review')
            for review in reviews:
                if len(review.text) > 2:
                    reviewList.append(review.text)

        f = open('movie_list.txt', 'w', encoding='utf8')
        for (index, review) in enumerate(reviewList):
            if index != len(reviewList) - 1:
                review += '\n'
            f.write(review)
        f.close()

        rating = sent_analysis.run('movie_list.txt', movieTitle.lower().split(' '))
        return JsonResponse({'title': movieTitle, 'rating': rating, 'imageURL': imageUrl, 'numReviews': len(reviewList), 'tomatometerScore': tomatometerScore})
        

