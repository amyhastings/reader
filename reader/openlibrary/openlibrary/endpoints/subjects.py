class SubjectsEndpoint:
    def __init__(self, client):
        self.client = client

    def get_subject(self, subject_key):
        """Fetch a specific subject by its key."""
        response = self.client.get(f"/subjects/{subject_key}.json")
        return response.json()

    def get_subjects(self):
        """Fetch a list of all subjects."""
        response = self.client.get("/subjects.json")
        return response.json()

    def get_books_by_subject(self, subject_key):
        """Fetch books associated with a specific subject."""
        response = self.client.get(f"/subjects/{subject_key}/works.json")
        return response.json()