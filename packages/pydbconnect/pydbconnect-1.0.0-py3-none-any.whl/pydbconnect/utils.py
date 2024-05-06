import json
from requests import Response


def decrypt_request_content(response: Response):
    return json.loads(response.content.decode(response.encoding))
