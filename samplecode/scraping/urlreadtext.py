"Retrieve a URL and decode response as a string"
# MCS 275 Spring 2022 David Dumas
from urllib.request import urlopen
import sys

def urlreadtext(url,*args,**kwargs):
    """
    Retrieve URL `url` and return the response body decoded as a string. If
    content-type specifies a charset, use that. Otherwise, attempt UTF-8
    decoding.  Returns the resulting string.

    Additional arguments are passed to `urllib.request.urlopen`.
    """
    with urlopen(url,*args,**kwargs) as res:
        # Get raw data (bytes)
        data = res.read()
        # Determine the encoding
        encoding = res.headers.get_content_charset()
        if encoding is None:
            # Danger: no encoding was specified in the headers
            # Try using UTF-8
            encoding = "UTF-8"

        # TODO: Detect if the response indicates a non-text content type, and if
        # so, raise an informative exception rather than just letting the
        # attempt to decode as a string fail.

        # Convert to string and return
        return data.decode(encoding)
        

if __name__=="__main__":
    if len(sys.argv) != 2:
        print("""Usage: {} URL
Note that many URLs contain characters that shells interpret specially, so
it may be necessary to enclose the URL in quotation marks to ensure it is
passed to this utility unchanged and as a single argument.""")
        exit(1)

    s = urlreadtext(sys.argv[1])
    print(s)