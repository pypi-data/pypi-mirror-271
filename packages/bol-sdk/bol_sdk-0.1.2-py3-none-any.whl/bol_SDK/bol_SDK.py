import csv
import json
try:
    from . import constants as CONSTANTS # For raspberry pi
except:
    import constants as CONSTANTS # For local development   
# ==== DEBUG =======
import os
# import numpy as np
import requests
import pprint
import time
from typing import List, Optional, Tuple, Union

# =============================================================================
#
# Calling the API credentials:
# ----------------------------
from dotenv import load_dotenv
load_dotenv()
client_id = os.environ.get('BOL_CLIENT_ID')
client_secret = os.environ.get('BOL_CLIENT_SECRET')
#
# ==============================================================================

# ==================

pp = pprint.PrettyPrinter(indent=4)

"""

Helpers

"""


def get_request_hearders(access_token):
    return  {'Authorization': f'Bearer {access_token}',
            'Content-Type': f'application/vnd.retailer.v{constants.API_VERSION}+json',
            'Accept': f'application/vnd.retailer.v{constants.API_VERSION}+json'}
    # return  {'Authorization': f'Bearer {access_token}',
    #     'Content-Type': f'application/json',
    #     'Accept': f'application/json' }


#split the date string into date integers
def split_date_string(date_string):
    date = date_string.split("+")[0]
    year = time.strptime(date,"%Y-%m-%dT%H:%M:%S").tm_year
    month = time.strptime(date,"%Y-%m-%dT%H:%M:%S").tm_mon
    day = time.strptime(date,"%Y-%m-%dT%H:%M:%S").tm_mday
    return day,month,year


"""

Authentication

"""
#get access_token
def get_access_token(client_id, client_secret):
    print('get_access_token')
    url = 'https://login.bol.com/token?grant_type=client_credentials'
    header = {
            "client_id": client_id,
            "client_secret": client_secret
        }
    r = requests.post(url,header)
    access_token = json.loads(r.text)['access_token']
    return access_token


"""

Orders

"""
#get a single order
def get_an_order(order_id,access_token):
    headers = get_request_hearders(access_token = access_token)
    order_request = 'https://api.bol.com/retailer/orders/'+str(order_id)
    order_info = json.loads(requests.get(order_request,headers = headers).text)
    return order_info

# #get all orders
def get_all_orders(status,access_token):
    page = 1
    all_orders = []
    headers = get_request_hearders(access_token = access_token)
    while(1):
        order_request = 'https://api.bol.com/retailer/orders?page='+str(page)+'&status='+status
        orders = json.loads(requests.get(order_request,headers = headers).text)
        if len(orders) != 0:
            for i in range(len(orders['orders'])):
                all_orders.append(orders['orders'][i])
        if len(orders) == 0:
            break
        page += 1
    return all_orders


# #get relevant orders' info from bol.com
def get_orders_by_date(day,month,year,status,access_token):
    orders = get_all_orders(status,access_token)
    relevant_orders = []
    for i in range(len(orders)):
        order = orders[i]
        # date_string = order['orderPlacedDateTime']
        # order_day,order_month,order_year = split_date_string(date_string)
        # if order_day == day and order_month == month and order_year == year:
        order_id = order['orderId']
        order_info = get_an_order(order_id,access_token)
        relevant_orders.append(order_info)
    return relevant_orders


"""

Offers (Products)

"""

#get an offer info (调试用)
def get_an_offer_info(offer_id: str, access_token: str) -> Tuple:
    """
    Fetch the details of the product data from Bol API.
    """
    headers = get_request_hearders(access_token = access_token)            
    order_request = 'https://api.bol.com/retailer/offers/'+offer_id
    resp = requests.get(order_request,headers = headers)
    status_code = resp.status_code
    offer_info = json.loads(resp.text)
    return status_code, offer_info

# Get offerId list
def get_offers_list(access_token, client_id, client_secret):
    #Step 1: Request an offer export file
    order_request = 'https://api.bol.com/retailer/offers/export'
    headers = get_request_hearders(access_token = access_token)
    post_data = json.dumps({ "format": "CSV" })
    while(1):    
        file_export_raw_response = requests.post(url     = order_request,
                                                 headers = headers,
                                                 data    = post_data )
        status, response = logApiResponse(file_export_raw_response)
        if status == 200 or status == 202:
            file_export_response = json.loads(response.text)
            break
        elif status == 429:
            continue
        elif status == 401:
            access_token = get_access_token(client_id, client_secret)
            headers      = get_request_hearders(access_token = access_token)
            continue
        else:
            os.sys.exit(f"An unexpected error occured while requesting an offer list. Status {status}: {response.json()}. Abort script.")
    print('(1/3) Successfully sent an export request to Bol.')

    #Step 2: 检索流程状态，只有变成success时才能往下处理 (checking status, only going further when showing "success")
    while(1):
        if 'processStatusId' in file_export_response:
            id = file_export_response['processStatusId']
        elif 'entityId' in file_export_response:
            id = file_export_response['entityId']
        else:
            os.sys.exit('Unexpected response, abort the process.')
        order_request  = f"https://api.bol.com/shared/process-status/{id}"
        # order_request  = f"https://api.bol.com/retailer/process-status/{id}"
        status_check_response = requests.get(url     = order_request,
                                             headers = headers )
        status, response = logApiResponse(status_check_response)
        if type(response) == str:
            print('[Bol API Error]', response)
            os.sys.exit('Unexpected error occured. Abort further execution.')
        process_status = json.loads(response.text)
        if status == 200 and process_status['status'] == 'SUCCESS':
            entityId = process_status['entityId']
            break
        elif status == 200 and process_status['status'] != 'SUCCESS':
            print(' ... waiting for Bol to finish the export process ...')
            time.sleep(10)
        elif status == 429:
            continue
        elif status == 401:
            access_token = get_access_token(client_id, client_secret)
            headers      = get_request_hearders(access_token = access_token)
            continue
        else:
            os.sys.exit(f"An unexpected error occured while requesting the process status of the offer list export. Status {status}: {response.json()}. Abort script.")
    print(f"(2/3) Successfully got the entity ID of the export request: {entityId}.")

    #Step 3: Retrieve an offer export file by offer export id
    while(1):
        order_request = f"https://api.bol.com/retailer/offers/export/{entityId}"
        export_headers = headers
        export_headers['Accept'] = f'application/vnd.retailer.v{constants.API_VERSION}+csv'
        offers = requests.get(order_request, headers = export_headers)
        status, response = logApiResponse(offers)
        if status == 200:
            offers_list = []
            reader = csv.reader(response.text.split('\n'), delimiter=',')
            index = 0
            for row in reader:
                if index != 0 and row != []:
                    offers_list.append(row)
                index += 1
            break
        elif status == 401:
            access_token = get_access_token(client_id, client_secret)
            headers      = get_request_hearders(access_token = access_token)
            continue
        elif status == 429:
            continue
        else:
            os.sys.exit(f"An unexpected error occured while requesting the process status of the offer list export. Status {status}: {response.json()}. Abort script.")
    print(f"(3/3) Successfully exported the offer list. {len(offers_list)} offer data retrieved.")
    return offers_list

# If you need update the offer_Id, use this one
#offerId_list = get_offers_list(access_token, client_id, client_secret)
#offerId_list = pd.DataFrame(offerId_list)
#offerId_list.to_csv("offerId_list.csv" ,header=0 ,index=0)


# Function 1
# Update the stock in Bol
# example: ean:'6935670512420' stock: 23

def update_stock(
        bol_offer_id:  str,
        stock_amount:  int,
        client_id:     str,
        client_secret: str,
        access_token: Optional[str] = ""
    ) -> None:
    """
    Identifies the product based on offer_id and update its stock amount. Upload attempts will be made up to 3 times. If the upload attempts are failed 3 times, it aborts updating.
    """
    ###
    # print('[Log] This is testing mode. Bol stock data is not updating...')
    # return 'SUCCESS'
    ###
    status       = 'UNKNOW'
    if not access_token:
        access_token = get_access_token(client_id, client_secret)

    # The maximum number of attempts to send out an update requst.
    update_attempt_count = 0
    headers = get_request_hearders(access_token = access_token)
    post_data = json.dumps({ 'amount': stock_amount,
                             'managedByRetailer' : False })
    while(update_attempt_count < constants.MAX_REQUEST_ATTEMPTS):
        order_request_url = f"https://api.bol.com/retailer/offers/" \
                            f"{bol_offer_id}/stock"
        # ------!!! DEV !!! ---------------------------------
        # return 'FAILURE'
        # return 'SUCCESS'
        # ---------------------------------------------------
        response_payload = json.loads(requests.put( order_request_url,
                                                    headers = headers,
                                                    data = post_data ).text)
        update_attempt_count += 1
        if 'status' not in response_payload or response_payload.get('status') == 'FAILURE':
            # An unexpected response.
            status = 'FAILURE'
            print('Unexpected failure during updating the stock on Bol. Abort further update..')
            print('-----payload-----')
            pp.pprint(post_data)
            print('-----------------')
            print('-----response----')
            pp.pprint(response_payload)
            print('-----------------')
            break
        elif response_payload['status'] == 401:
            time.sleep(5)
            access_token = get_access_token(client_id, client_secret)
            headers      = get_request_hearders(access_token = access_token)
            continue
        elif response_payload['status'] == 'PENDING':
            status = 'SUCCESS'
            print(status)
            break
        else:
            # ?
            status = 'FAILURE'
            print('Unexpected failure during updating the stock on Bol for unknown ends. Abort further update..')
            print('-----payload-----')
            pp.pprint(post_data)
            print('-----------------')
            print('-----response----')
            pp.pprint(response_payload)
            print('-----------------')
            break

    if status != 'SUCCESS':
        status = 'FAILURE'
        print(f"{status}, {constants.MAX_REQUEST_ATTEMPTS - 1} attempts were made to upload the stock of product {bol_offer_id} on Bol, but all failed. Abort updating this product.")
        pp.pprint(response_payload)

    return status

#test
#update_stock(6935670512420,23)


# Function 2
# Update the price in Bol
# def update_price(ean,price):
#     offerId_list = pd.read_csv('offerId_list.csv', header=None)
#     #get offerId using ean
#     for i in range(len(offerId_list)):
#         if offerId_list[1][i] == ean:
#             offer_id = offerId_list[0][i]
#             print('find it')
#     #Bol price update
#     status = 'UNKNOW'
#     headers = get_request_hearders(access_token = access_token)
#     post_data = json.dumps({"pricing": {"bundlePrices": [{"quantity": 1,"unitPrice": price}]} })
#     while(1):       
#         order_request = 'https://api.bol.com/retailer/offers/'+offer_id+'/price'
#         update_response = json.loads(requests.put(order_request,headers = headers, data = post_data).text)
#         if update_response['status'] == 'PENDING':
#             status = 'SUCCESS'
#             print(status)
#             break
#         if update_response['status'] == 'FAILURE':
#             status = 'FAILURE'
#             print(status)
#             break
#     return status

#update_price(6935670512420,629)
def logApiResponse (response, abort_when_error = True):
    """
    The function takes a response from API and handle exceptions. If the status code 200, the status code and a successful response is returned. If the other status code is returned, the function returns only the status code.
    """
    status = response.status_code
    if status == 429: # Rate limited.
        print(f"Bol exporting offer data, rate limited. Try again after {response.headers['Retry-After']} seconds...")
        time.sleep(int(response.headers["Retry-After"]))
        return status, ""
    elif status == 401 or status == 403: # Authentication token expired.
        print('Authenticaton token expired. Regenerate the access token...')
        time.sleep(20)
        return status, ""
    elif status == 200 or status == 201 or status == 202 or status == 204:
        return status, response
    elif abort_when_error:
        os.sys.exit(f"Encountered to unexpected response. Status code {status}: {response.json()}. Abort further process.")
    elif not abort_when_error:
        print(f"Encountered an error while retrieving the API response. Status code {status}: {response.json()}.")
        return status, ""


"""

Rate Limiting

"""
def get_rate_limits() -> Tuple:
    """
    Requests the list of rate limiting in each endpoint.
    """
    rate_limint_url = 'https://api.bol.com/retailer/public/ratelimits'
    response = requests.get(rate_limint_url)
    status_code = response.status_code
    rate_limit_list = response.json()
    return (status_code, rate_limit_list)


def get_rate_limit_by_path(path: str) -> Union[None, List]:
    """
    Returns the rate limiting info of the given path.

    params
    ------
    path       [str]    The path to the specific API endpoint. Path should be
                        the string after https://api.bol.com, including the leading '/'. Dynamic routes accept '*' as a place holder.
                        e.g.) "/retailer/shipping-labels", "/retailer/returns/*"
    returns
    -------
    rate_limit [List]   Rate limit data of a specific API endpoint.
                        e.g.)
                        {
                          "path" : "/retailer/shipments/*",
                          "methods" : "GET, OPTIONS, HEAD",
                          "maxCapacity" : "14",
                          "timeToLive" : "1",
                          "timeUnit" : "MINUTES"
                        }
    None        [None]  When an error occurs, None will be returned.

    """
    (status_code, rate_limit_list) = get_rate_limits()
    if status_code != 200:
        return None
    rate_limit = list(filter(
                    lambda endpoint_info: endpoint_info['path'] == path,
                    rate_limit_list))
    if len(rate_limit) > 1:
        return rate_limit[0]
    return None
