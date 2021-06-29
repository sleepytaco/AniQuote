import requests
from main.models import Quote


# returns a list of all the possible anime available
def get_available_anime():
    response = requests.get('https://animechan.vercel.app/api/available/anime')

    anime_list = list(response.json())

    return anime_list


# saves a quote in the database, if it does not exist
# if the quote already exists, increment it's views
def save_quote(quote):
    if Quote.objects.filter(quote__exact=quote["quote"]).count() == 0:
        q = Quote(anime=quote["anime"], character=quote["character"], quote=quote["quote"])
        q.save()
    else:
        q = Quote.objects.get(quote__exact=quote["quote"])
        q.views += 1
        q.save(update_fields=['views'])

    return q
