from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import re
from bs4 import BeautifulSoup
from . import sent_analysis


def index(request):
    return render(request, 'reviews/index.html')
# Create your views here.

def movie(request):
    if request.method == 'GET':
        movieTitle = request.GET.get('title')
        if not movieTitle:
            response = JsonResponse({'message': 'Invalid request: title query invalid'}, status = 400)
            return response
        res = requests.get('https://google.com/search?q=' + movieTitle + '%20site:rottentomatoes.com/m')
        googleHtml = BeautifulSoup(res.text, 'html.parser')
        searchResults = googleHtml.select('#search a')
        link = None
        for result in searchResults:
            if 'https://www.rottentomatoes.com/m/' in result['href']:
                link = result['href'].split('?q=')[1].split('&')[0]
                if '/reviews' not in result['href']:
                    link += '/reviews'
                break
        if link is None:
            response = JsonResponse({'message': 'Internal server error: Unable to find movie'}, status = 500)
            return response

        res = requests.get(link)
        rtHtml = BeautifulSoup(res.text, 'html.parser')
        res = requests.get(link.replace('/reviews', ''))
        rtHomeHtml = BeautifulSoup(res.text, 'html.parser')
        totalPages = int(rtHtml.select('#reviews span.pageInfo')[0].text.split(' ').pop())
        imageUrl = rtHtml.select('.panel-body.content_body img')[0]['src']
        movieTitle = rtHtml.select('.panel-body.content_body h2 > a')[0].text
        reviews = rtHtml.select('#reviews .the_review')
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
        

