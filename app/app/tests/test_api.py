import sys
from pprint import pprint


def test_get_song(client):
    response = client.get("/")
    pprint('+++++++++++++++++++++++++++++++++++++', stream=sys.stderr)
    pprint(response, stream=sys.stderr)
    assert response.status_code == 200