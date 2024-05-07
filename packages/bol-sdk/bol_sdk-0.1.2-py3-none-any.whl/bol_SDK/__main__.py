import os
import pprint

from bol_SDK import bol_SDK as bol
from dotenv import load_dotenv


def main():
  load_dotenv()
  pp = pprint.PrettyPrinter(indent=4)

  client_id     = os.environ.get('BOL_CLIENT_ID')
  client_secret = os.environ.get('BOL_CLIENT_SECRET')
  access_token  = bol.get_access_token(client_id, client_secret)
  # orders = bol.get_orders_by_date('09', '7', '2022', 'ALL', access_token)
  # offers = bol.get_offers_list(access_token=access_token, client_id=client_id, client_secret=client_secret)
  result = bol.update_stock(bol_offer_id = "6b5c0bd4-003d-4890-81af-f1bb87997381", 
                            stock_amount = 14,
                            client_id=client_id, 
                            client_secret=client_secret, 
                            access_token=access_token)
  print('-----------------')
  pp.pprint(result)


if __name__ == '__main__':
  main()