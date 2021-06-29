from django.http import HttpResponse
from django.shortcuts import render
import requests
from django.template import loader
from random import randrange
from .models import Quote
from .util import *


def index(request):
    most_liked_quotes = Quote.objects.filter(likes__gt=0).order_by("-likes")[:3]
    anime_list = get_available_anime()

    return render(request, 'index.html',
                  {
                      "quotes": most_liked_quotes,
                      "anime_list": anime_list
                  })


def get_random_quote(request):
    response = requests.get('https://animechan.vercel.app/api/random')

    if response.status_code == 429:  # if default rate limit is hit
        return HttpResponse("""
        <h4>Default rate limit of 100 requests per hour has been reached :(</h4>
        <a class="button button" href="#quote" hx-get="get-random-quote" hx-target="#quote-result" hx-indicator="#quote-load-indicator">
            RETRY
        </a>
        """)

    quote = response.json()

    q = save_quote(quote)

    return HttpResponse(loader.get_template("quote.html").render({"quote": q}))


def get_specific_quote(request):
    if request.method == "POST":
        anime = request.POST['selectAnimeInput']

        response = requests.get(f'https://animechan.vercel.app/api/quotes/anime?title={anime}')

        if response.status_code == 429:  # if default rate limit is hit
            return HttpResponse("""
                <h4>Default rate limit of 100 requests per hour has been reached :(</h4>
                <a class="button button" href="#quote" hx-get="get-random-quote" hx-target="#quote-result" hx-indicator="#quote-load-indicator">
                    RETRY
                </a>
                """)

        quotes = list(response.json())
        quote = quotes[randrange(len(quotes))]  # pick a random quote from the quotes list

        q = save_quote(quote)

        return HttpResponse(f"""
            <h4>"{ q.quote }"</h4>
            <p>~ { q.character }, { q.anime }</p>
            <h4>
            <i class="far fa-heart" hx-get="like-quote-{ q.pk }" hx-swap="outerHTML" hx-indicator="#quote-load-indicator"></i>
            </h4>
        """)
    else:
        response = requests.get('https://animechan.vercel.app/api/random')

        if response.status_code == 429:  # if default rate limit is hit
            return HttpResponse("""
                <div id="retry-result">
                <h4>Default rate limit of 100 requests per hour has been reached :(</h4>
                <a class="button button" href="#quote" hx-get="get-random-quote" hx-target="#retry-result" hx-indicator="#quote-load-indicator">
                    RETRY
                </a>
                </div>
                """)

        quote = response.json()
        q = save_quote(quote)

        return HttpResponse(f"""
                    <h4>"{q.quote}"</h4>
                    <p>~ {q.character}, {q.anime}</p>
                    <h3>
                    <i class="far fa-heart" hx-get="like-quote-{ q.pk }" hx-swap="outerHTML" hx-indicator="#quote-load-indicator"></i>
                    </h3>
                """)


def like_quote(request, id):
        quote = Quote.objects.get(pk=id)
        quote.likes += 1
        quote.save(update_fields=['likes'])

        return HttpResponse(f"""
            <i class="fas fa-heart" hx-get="like-quote-{quote.pk}" hx-swap="outerHTML" hx-indicator="#quote-load-indicator"></i>
        """)


def unlike_quote(request, id):
    quote = Quote.objects.get(pk=id)
    quote.likes -= 1
    quote.save(update_fields=['likes'])

    return HttpResponse(f"""
            <i class="far fa-heart" hx-get="unlike-quote-{quote.pk}" hx-swap="outerHTML" hx-indicator="#quote-load-indicator"></i>
        """)
