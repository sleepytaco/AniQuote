import requests
from .models import Quote

RATE_LIMIT_ERROR = """
                <div id="retry-result">
                <h4>Default rate limit of <a href="https://animechan.vercel.app/guide#pagination" style="color: black; text-decoration: none; border-bottom: 3px red dashed;">100 requests per hour</a> has been reached :(</h4>
                
                <button class="button" onclick="location.reload();">Refresh Page</button>
                </div>
                """


# returns a list of all the possible anime available
def get_available_anime():
    response = requests.get('https://animechan.vercel.app/api/available/anime')

    if response.status_code == 429:  # default request limit of 100 was reached
        return ["N/A"]

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
