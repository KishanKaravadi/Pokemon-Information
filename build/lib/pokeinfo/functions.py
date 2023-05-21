import requests
import os
import shelve


BASE_URL = "http://pokeapi.co/api/v2"


def get_default_cache():
    """Get the default cache location.

    Adheres to the XDG Base Directory specification, as described in
    https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html

    :return: the default cache directory absolute path
    """

    xdg_cache_home = os.environ.get('XDG_CACHE_HOME') or \
        os.path.join(os.path.expanduser('~'), '.cache')

    return os.path.join(xdg_cache_home, 'pokebase')


API_CACHE = get_default_cache()


def api_url_new(endpoint, resource_id=None, subresource=None):

    if resource_id is not None:
        if subresource is not None:
            return "/".join([BASE_URL, endpoint, str(resource_id), subresource, ""])

        return "/".join([BASE_URL, endpoint, str(resource_id), ""])

    return "/".join([BASE_URL, endpoint, ""])


def _call_api_url(url):

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    return data


def get_data_ur(url, **kwargs):
    # print("Hi")
    # if not kwargs.get("force_lookup", False):
    #     try:
    #         data = load_uri(url)
    #         return data
    #     except KeyError:
    #         pass

    # data = _call_api_url(url)
    # save_uri(data, url)

    # return data
    print("Hi")
    return None


def get_hi(url):
    print("Hi")
    return None


def save_uri(data, uri):

    if data == dict():    # No point in saving empty data.
        return None

    if not isinstance(data, (dict, list)):
        raise ValueError('Could not save non-dict data')

    try:
        with shelve.open(API_CACHE) as cache:
            cache[uri] = data
    except OSError as error:
        if error.errno == 11:  # Cache open by another person/program
            # print('Cache unavailable, skipping save')
            pass
        else:
            raise error

    return None


def load_uri(uri):

    try:
        with shelve.open(API_CACHE) as cache:
            return cache[uri]
    except OSError as error:
        if error.errno == 11:
            # Cache open by another person/program
            # print('Cache unavailable, skipping load')
            raise KeyError("Cache could not be opened.")
        else:
            raise
