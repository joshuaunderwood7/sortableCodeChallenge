
import json
import statistics
import multiprocessing
from pprint import pprint

def currency_conversion(currency_type, listing_price):
    """
    print(set([l[u'currency'] for l in listings]))
    gives me : {'EUR', 'GBP', 'USD', 'CAD'}
    which I could fetch up to date currency rates, but for the sake of
    having a more predictable result, I'll just go with this...
    """
    if   currency_type == "CAD" : return listing_price # * 1
    elif currency_type == "USD" : return listing_price * 1.28
    elif currency_type == "GBP" : return listing_price * 1.82
    elif currency_type == "EUR" : return listing_price * 1.44
    else                        : return listing_price # How could this happen?

def simple_recall_filter(product, listing):
    listing_title        = listing[u'title'].upper()
    product_model        = product[u'model'].upper()
    listing_manufacturer = listing[u'manufacturer'].upper()
    product_manufacturer = product[u'manufacturer'].upper()

    model_in_listing       = product_model in listing_title
    manufacturer_in_lising = listing_manufacturer == product_manufacturer

    return all([ model_in_listing
               , manufacturer_in_lising
               ])

def stat_recal_filter(prod_listing):
    if len(prod_listing) < 3 : return prod_listing
    prices = [ currency_conversion(l[u'currency'], float(l[u'price'])) 
               for l in prod_listing]
    l_median = statistics.median(prices)
    l_stddev = statistics.stdev(prices)

    prod_listing = [ l for l in prod_listing 
                        if float(l[u'price']) < (l_median - l_stddev)
                    ]
    return prod_listing


def mapable_build_result(products, listings):
    results = list()
    for product in products:
        prod_listing = stat_recal_filter ([ l for l in listings 
                         if simple_recall_filter(product, l) ])
        
        result = json.dumps( { u'product_name' : product[u'product_name'] 
                             , u'listings'     : prod_listing
                             }
                             , ensure_ascii=False
                           )
        results.append(result)
    return results


def main():
    with open('./listings.txt', encoding='utf-8', mode='r') as fileIn:
        listings = [json.loads(line) for line in fileIn]

    with open('./products.txt', encoding='utf-8', mode='r') as fileIn:
        products = [json.loads(line) for line in fileIn]

    results = mapable_build_result(products, listings)

    with open('./output.txt', encoding='utf-8', mode='w') as fileOut:
        fileOut.writelines(map(lambda r: r + '\n', results))


if __name__=='__main__':
    main()


