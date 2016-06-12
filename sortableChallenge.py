
import json
from pprint import pprint

def main():
    results = list()
    with open('./listings.txt', encoding='utf-8', mode='r') as fileIn:
        listings = [json.loads(line) for line in fileIn]
    with open('./products.txt', encoding='utf-8', mode='r') as fileIn:
        for product in (json.loads(line) for line in fileIn):
            prod_listing = [ listing 
                for listing in listings if all(
                    [ product[u'product_name'].replace('_',' ').upper() in listing[u'title'].upper() 
                    , product[u'manufacturer'].upper() == listing[u'manufacturer'].upper()
                    ]) ]
            result = json.dumps( { u'product_name' : product[u'product_name'] 
                                 , u'listings'     : prod_listing
                                 }
                               , ensure_ascii=False
                               )
            results.append(result)
    with open('./output.txt', encoding='utf-8', mode='w') as fileOut:
        fileOut.writelines(map(lambda r: r + '\n', results))


if __name__=='__main__':
    main()


