# Wiki API for images
WIKI_IMAGE = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

# Wiki API for page summary
WIKI_SUMMARY = 'https://en.wikipedia.org/w/api.php?action=query&' \
               'format=json&prop=extracts&exintro=true&explaintext=true&titles='

# To mimic request from web browser
HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537'}
