from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render
import praw
import os
import json
from .models import Search
from django.contrib.auth.decorators import login_required

# Create your views here.


class RedditPost:
    def __init__(self, forum, submission):
        self.subreddit = forum
        self.title = submission.title
        self.score = submission.score
        self.comments = submission.num_comments
        self.link = submission.permalink
        self.date = submission.created_utc
        self.body = submission.selftext
        self.id = submission.id
        self.weight = 0
        self.contains = []

    def __hash__(self):
        return hash(self.id + str(self.date))


def find_matches(subreddits, searchterms):
    r = praw.Reddit(user_agent=os.getenv('USER_AGENT'),
                    client_id=os.getenv('CLIENT_ID'), client_secret=os.getenv('CLIENT_SECRET'))

    posts = set()

    for subreddit in subreddits:
        sr = r.subreddit(subreddit)
        for submission in sr.hot(limit=100):
            if not submission.selftext:
                continue

            found = False
            for term in searchterms:
                if term in submission.title.casefold() or term in submission.selftext.casefold():
                    found = True

            if found:
                posts.add(RedditPost(subreddit, submission))
    return posts


def score_posts(posts, searchterms):
    maxscore = 1
    mostrecent = 1
    mostcomments = 1
    for post in posts:
        if post.score >= maxscore:
            maxscore = post.score
        if post.date >= mostrecent:
            mostrecent = post.date
        if post.comments >= mostcomments:
            mostcomments = post.comments
        for term in searchterms:
            if term in post.body.casefold() or term in post.title.casefold():
                post.contains.append(term)

    for post in posts:
        post.weight = (len(post.contains) / len(searchterms)) * .65
        post.weight += (post.score / maxscore) * .05
        post.weight += (post.date / mostrecent) * .25
        post.weight += (post.comments / mostcomments) * .05

    weighted_posts = sorted(
        posts, key=lambda x: x.weight, reverse=True)
    return weighted_posts


@login_required
def reddit_search(request):

    if request.method == 'POST':
        json_data = json.loads(request.body)
        Search.objects.create(
            searchname=json_data['searchname'],
            subreddits=json_data['subreddits'],
            searchterms=json_data['searchterms'],
            user=request.user,
        )

    searches = request.user.searches.all()

    results = []

    for search in searches:
        subreddits = search.subreddits.split(',')
        searchterms = search.searchterms.split(',')

        posts = find_matches(subreddits, searchterms)
        weighted_posts = score_posts(posts, searchterms)

        json_formatted_results = []
        for post in weighted_posts:
            post = {
                'title': post.title,
                'link': 'http://reddit.com' + post.link,
                'subreddit': post.subreddit,
                'matches': post.contains,
                'date': post.date,
                'score': int(post.weight * 100),
                'postid': post.id,
            }
            json_formatted_results.append(post)
        results.append({
            'searchname': search.searchname,
            'subreddits': ','.join(subreddits),
            'searchterms': ','.join(searchterms),
            'posts': json_formatted_results,
            'hits': len(json_formatted_results),
            'id': search.id,
        })

    return JsonResponse(results, safe=False)
    # return render(request, 'redditsearch/searchresults.html', {'results': results})


def search_delete(request, id):
    search = get_object_or_404(Search, id=id)
    search.delete()
    return JsonResponse({})


def edit_search(request, id):
    search_delete(request, id)
    reddit_search(request)


@login_required
def dashboard(request):
    return render(request, 'redditsearch/dashboard.html')


@login_required
def test(request):
    return render(request, 'redditsearch/test.html')


def layout(request):
    return render(request, 'layout.html')

def welcome(request):
    return render(request, 'redditsearch/welcome.html')
