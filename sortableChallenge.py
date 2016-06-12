
import json

def recall_filter(product, listing):
    listing_title = listing[u'title'].upper()
    product_name  = product[u'product_name'].upper()

    name_in_listing = any([ product_name in listing_title
                          , product_name.replace('_',' ')in listing_title
                          , all([pn + ' ' in listing for pn in product_name.split('_')])
                          , all([pn + ' ' in listing for pn in product_name.split('-')])
                          ])

    manufacturer_in_lising = product[u'manufacturer'].upper() == listing[u'manufacturer'].upper()

    return all([ name_in_listing
               , manufacturer_in_lising
               ])

def main():
    results = list()
    with open('./listings.txt', encoding='utf-8', mode='r') as fileIn:
        listings = [json.loads(line) for line in fileIn]
    with open('./products.txt', encoding='utf-8', mode='r') as fileIn:
        for product in (json.loads(line) for line in fileIn):
            prod_listing = filter(lambda l: recall_filter(product, l), listings)
            result = json.dumps( { u'product_name' : product[u'product_name'] 
                                 , u'listings'     : list(prod_listing)
                                 }
                               , ensure_ascii=False
                               )
            results.append(result)
    with open('./output.txt', encoding='utf-8', mode='w') as fileOut:
        fileOut.writelines(map(lambda r: r + '\n', results))


if __name__=='__main__':
    main()


