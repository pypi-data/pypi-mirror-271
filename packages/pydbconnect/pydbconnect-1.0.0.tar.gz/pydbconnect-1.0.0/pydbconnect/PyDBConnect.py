import requests
import json

from requests import Response


def decrypt_request_content(response: Response):
    return json.loads(response.content.decode(response.apparent_encoding))


class connection:
    def __init__(self, hostname: str, project: str, password: str):
        self.hostname = hostname
        self.project = project
        self.password = password

    def ping_db(self) -> Response:
        """
        Pings the database server to check if there is a proper connection available
        Returns: Response
        """
        return requests.get(self.hostname)

    def get_collections(self) -> any:
        """
        Returns a list of collections for the given project (list[str])

        If the response errors out it will return a Response object
        """
        response = requests.get(
            self.hostname + "/get/" + self.project + "/" + self.password
        )
        if response.status_code != 200:
            return response
        return decrypt_request_content(response)

    def get_collection(self, collection: str) -> any:
        """
        Returns the data of the given collection (dict)

        If the response errors out it will return a Response object
        """
        response = requests.get(
            self.hostname
            + "/get/"
            + self.project
            + "/"
            + collection
            + "/"
            + self.password
        )
        if response.status_code != 200:
            return response
        return decrypt_request_content(response)

    def get_document(self, collection: str, document: str) -> any:
        """
        Returns the data of the given document (dict)

        If the response errors out it will return a Response object
        """
        response = requests.get(
            self.hostname
            + "/get/"
            + self.project
            + "/"
            + collection
            + "/"
            + document
            + "/"
            + self.password
        )
        if response.status_code != 200:
            return response
        return decrypt_request_content(response)

    def create_document(self, collection: str, document_id: str, content: dict) -> any:
        """
        Creates a new document in the given collection

        Returns: contents of the new document (dict)

        If the response errors out it will return a Response object
        """
        response = requests.post(
            self.hostname
            + "/create-document/"
            + self.project
            + "/"
            + collection
            + "/"
            + document_id
            + "/"
            + self.password,
            json=content,
        )
        if response.status_code != 200:
            return response
        return decrypt_request_content(response)

    def update_document(self, collection: str, document_id: str, content: dict) -> any:
        """
        Updates an existing document in the given collection

        Returns: contents of the updated document (dict)

        If the response errors out it will return a Response object
        """
        response = requests.put(
            self.hostname
            + "/update-document/"
            + self.project
            + "/"
            + collection
            + "/"
            + document_id
            + "/"
            + self.password,
            json=content,
        )
        if response.status_code != 200:
            return response
        return decrypt_request_content(response)

    def delete_document(self, collection: str, document_id: str) -> Response:
        """
        Deletes document from the collection

        Returns: Response
        """
        return requests.delete(
            self.hostname
            + "/delete-document/"
            + self.project
            + "/"
            + collection
            + "/"
            + document_id
            + "/"
            + self.password
        )

    def create_collection(self, collection: str) -> Response:
        """
        Creates a new collection in the given project.

        Returns: Response
        """
        return requests.post(
            self.hostname
            + "/create-collection/"
            + self.project
            + "/"
            + collection
            + "/"
            + self.password
        )

    def delete_collection(self, collection: str) -> Response:
        """
        Deletes the given collection from the project.

        Returns: Response
        """

        return requests.delete(
            self.hostname
            + "/delete-collection/"
            + self.project
            + "/"
            + collection
            + "/"
            + self.password
        )
