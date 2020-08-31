from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
from django.http import HttpResponse
from django.conf import settings
import json
from datetime import datetime
import itertools
from collections import defaultdict
# Create your views here.

# Fetches all news from the json file
def get_news():
    with open(settings.NEWS_JSON_PATH, 'r') as json_file:
        return json.load(json_file)

# Orders json_list by most recent
def order_recent(json_list):
    def simple_date_fun(date):
        return datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")

    date_news = {}
    for news in json_list:
        news_date = simple_date_fun(news['created'])
        if news_date in date_news.keys():
            date_news[news_date].append(news)
        else:
            date_news[news_date] = [news]
    return date_news

# Handles filtering of news based on keywords on the home page
def search_news(req, news_list):
    search = req.GET
    if search != {}:
        search = search['q']
        news_list = list(filter(lambda x: search.lower() in x['title'].lower(), news_list))
    return news_list


class MainPageView(View):
    def redirect_view(request):
        return HttpResponseRedirect("news/")

    def get(self, request, *args, **kwargs):
        return render(request, 'news/default.html')

# Gets the news based on the blog_id
class ViewNews(View):
    def get(self, request, blog_id, *args, **kwargs):
        news_list = get_news()
        for news in news_list:
            if news['link'] == int(blog_id):
                return render(request, 'news/news.html', context=news)

# The home page that links to the actual news
class ViewHome(View):
    def get(self, request, *args, **kwargs):
        all_news = search_news(request, get_news())
        # Organizes news based on latest
        all_news.sort(key=lambda x: datetime.strptime(x['created'], "%Y-%m-%d %H:%M:%S"), reverse=True)
        date_news = order_recent(all_news)
        
        context = {'all_pages': date_news}
        return render(request, "news/home.html", context=context)

# For creating new news 
class CreateNewsView(View):
    all_news = get_news()

    def get(self, request, *args, **kwargs):
        return render(request, 'news/create.html')

    # Appends the newly created news in the right format by overwriting the current file
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        text = request.POST.get('text')
        link = self.all_news[-1]['link'] + 1
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        create_news = {"created": time, "text": text, "title": title, "link": link}
        self.all_news.append(create_news)
        with open(settings.NEWS_JSON_PATH, 'w') as json_news:
            json.dump(self.all_news, json_news)
        return redirect('/news/')
