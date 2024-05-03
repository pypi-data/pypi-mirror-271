import json

version_json = '''
{
 "date": "2024-05-02T00:00:00-0000",
 "dirty": false,
 "error": null,
 "full-revisionid": "a729a823ca99e9e15918bdb4d8a46267b8e4be11",
 "version": "1.1.2"
}
'''  # END VERSION_JSON

def get_versions():
    return json.loads(version_json)
