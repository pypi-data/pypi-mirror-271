import json

version_json = '''
{
 "date": "2024-05-02T00:00:00-0000",
 "dirty": false,
 "error": null,
 "full-revisionid": "f58709dae8992333a2584ffeab98f2fc5c933ea7",
 "version": "2.2.1"
}
'''  # END VERSION_JSON

def get_versions():
    return json.loads(version_json)
