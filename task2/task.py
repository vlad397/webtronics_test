import urllib.parse


def url_encoder(url: str):
    urllib.parse.unquote
    return urllib.parse.quote(url, safe="")


print(url_encoder('https://www.rd.com/list/interesting-facts/'))

# output -> https%3A%2F%2Fwww.rd.com%2Flist%2Finteresting-facts%2F
