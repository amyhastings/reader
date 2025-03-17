import math

class searchResult:
    def __init__(self, _count, _results):
        self.count = _count
        self.results = _results
        self.pages = range(1, (math.ceil(self.count / 100)+1))
        for result in self.results:
            result["key"] = result["key"].split("/")[2]

class OpenLibraryClient:
    BASE_URL = "https://openlibrary.org"

    def __init__(self):
        pass

    def _get(self, endpoint, params=None):
        import requests

        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_books(self, params=None):
        return self._get("/books", params)

    def get_authors(self, params=None):
        return self._get("/authors", params)

    def get_subjects(self, params=None):
        return self._get("/subjects", params)

    def search_book(self, searchString, page):
        olResponse = self._get("/search.json", {'title': searchString, 'fields': 'key,title,author_name,isbn,first_publish_year,edition_count,cover_i,', 'page': page})
        result = searchResult(olResponse['num_found'], olResponse['docs'])
        return result
    
    def search_author(self, searchString, page):
        olResponse = self._get("/search.json", {'author': searchString, 'fields': 'key,title,author_name,isbn,first_publish_year,edition_count,cover_i', 'page': page})
        result = searchResult(olResponse['num_found'], olResponse['docs'])
        return result
    
    def get_author_by_id(self, author_id):
        return self._get("/authors/%s.json" % author_id)
    
    def get_pub_date_and_editions(self, key):
        olResponse = self._get("/search.json", {'q': key, 'fields': 'key,first_publish_year,edition_count'})
        for result in olResponse['docs']:
            if result['key'] == "/works/%s" % key:
                return { 'first_publish_year': result['first_publish_year'], 'edition_count': result['edition_count']}
        return { 'first_publish_year': 'unknown', 'edition_count': 'unknown' }
    
    def get_book_by_key(self, key):
        book_json = self._get("/works/%s.json" % key)
        authors = []
        for author in book_json['authors']:
            author_id = author['author']['key'].split("/")[2]
            author_json = self.get_author_by_id(author_id)
            authors.append(author_json['name'])
        book_json['authors'] = authors
        if 'description' in book_json.keys():
            if type({}) == type(book_json['description']):
                book_json['description'] = book_json['description']['value']
        else:
            book_json['description'] = ""
        book_json['olid'] = key
        return book_json
    
    def get_book_ratings(self, key):
        rating_json = self._get("/works/%s/ratings.json" % key)
        return rating_json['summary']['average']