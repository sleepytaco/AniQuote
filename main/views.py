from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from random import randrange
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
        return HttpResponse(RATE_LIMIT_ERROR)

    quote = response.json()

    q = save_quote(quote)

    return HttpResponse(loader.get_template("quote.html").render({"quote": q}))


def get_specific_quote(request):
    if request.method == "POST":
        anime = request.POST['selectAnimeInput']

        quotes = []
        page = 1
        while True:
            response = requests.get(f'https://animechan.vercel.app/api/quotes/anime?title={anime}&page={page}')

            if response.status_code == 404:  # no quotes found on this page
                break

            if response.status_code == 429:  # if default rate limit is hit
                return HttpResponse(RATE_LIMIT_ERROR)

            quotes += list(response.json())
            page += 1

            if page == 3:  # limit to just first 2 pages
                break

        quote = quotes[randrange(len(quotes))]  # pick a random quote from the quotes list

        q = save_quote(quote)

        return HttpResponse(f"""
            <h4>"{q.quote}"</h4>
            <p>~ {q.character}, {q.anime}</p>
            <h4>
            <i class="far fa-heart" hx-get="like-quote-{q.pk}" hx-swap="outerHTML" hx-indicator="#quote-load-indicator"></i>
            </h4>
        """)
    else:
        response = requests.get('https://animechan.vercel.app/api/random')

        if response.status_code == 429:  # if default rate limit is hit
            return HttpResponse(RATE_LIMIT_ERROR)

        quote = response.json()
        q = save_quote(quote)

        return HttpResponse(f"""
                    <h4>"{q.quote}"</h4>
                    <p>~ {q.character}, {q.anime}</p>
                    <h3>
                    <i class="far fa-heart" hx-get="like-quote-{q.pk}" hx-swap="outerHTML" hx-indicator="#quote-load-indicator"></i>
                    </h3>
                """)


def like_quote(request, pk):
    quote = Quote.objects.get(pk=pk)
    quote.likes += 1
    quote.save(update_fields=['likes'])

    return HttpResponse(f"""
            <i class="fas fa-heart" hx-get="unlike-quote-{quote.pk}" hx-swap="outerHTML" hx-indicator="#quote-load-indicator"></i>
        """)


def unlike_quote(request, pk):
    quote = Quote.objects.get(pk=pk)
    quote.likes -= 1
    quote.save(update_fields=['likes'])

    return HttpResponse(f"""
            <i class="far fa-heart" hx-get="like-quote-{quote.pk}" hx-swap="outerHTML" hx-indicator="#quote-load-indicator"></i>
        """)
