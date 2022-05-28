from serpapi import GoogleSearch
params = {
    "engine": "google_scholar_author",
    "author_id": "I8Wm7XoAAAAJ",
    "api_key": "5693539bbd7f27e4de0624ca01bc9ad9ecba73199cbc2ce132e589daa15f8e4a",
    "start": 0,
    "num": "100"
}
search = GoogleSearch(params)
results = search.get_dict()
print(results)

