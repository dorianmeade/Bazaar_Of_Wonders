#####################################################################################################################
# Currently grabs the listings for a few products and prints the results. We will most likely want to replace the   #
# prints with function calls that save to the DB.                                                                   #
#                                                                                                                   #
# We might also want to make this into a function so it can be called when it's needed and passed parameters.       #
#                                                                                                                   #
# It could be useful to be able to pass in a card name and then return results just for that card.                  #
#####################################################################################################################

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

# For now, I'm starting at an arbitrary product_ID. If we want data for all the products we'll start from 0.
product_ID = 214823

# Base URL for retrieving TCGPlayer listing data
url = 'https://shop.tcgplayer.com/productcatalog/product/getpricetable?captureFeaturedSellerData=True&' \
      'pageSize=100&productId='

# Iterates through the specified products. There doesn't appear to be any product_IDs greater than 240000 currently.
while product_ID < 214923:
    product_url = url + str(product_ID)  # The product_ID is concatenated to the base URL

    req = Request(product_url, headers={'User-Agent': 'Mozilla/5.0'})  # Create a request object

    # Retrieves the response for the above request in the form of HTML.
    # The try except block is used in case a product ID doesn't exist.
    try:
        page = urlopen(req).read()
    except:
        product_ID += 1
        continue

    # Creates a BeautifulSoup object with the retrieved HTML
    soup = BeautifulSoup(page, 'html.parser')

    product_line = '"product_line": "Magic"'
    product_line_check = str(soup).find(product_line)

    # Check if the product_line is Magic. If not, continue to the next product.
    if product_line_check == -1:
        product_ID += 1
        continue

    # Finds HTML elements with the desired listing data
    listings = soup.find_all('script', attrs={'type': 'text/javascript'})

    # Checks if there are no listings for a product
    if not listings:
        product_ID += 1
        continue

    listings.pop(0)  # This pop gets rid of some junk data that was captured in the above find_all

    index = 0
    more_listings = True

    # Iterates through all the listings for a particular product
    while more_listings:
        try:
            result = listings[index].contents[0]
            print(result)
            index += 1
        except:
            more_listings = False

    product_ID += 1

