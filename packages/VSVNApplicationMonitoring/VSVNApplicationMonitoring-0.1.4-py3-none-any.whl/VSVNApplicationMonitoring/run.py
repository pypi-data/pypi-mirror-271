
import requests


def saveActiveUser(data_user : any, api_url: any):
    try:
        # Send a POST request to the specified URL with the data
        url = api_url + '/applications/create-active-user'
        response = requests.post(url, json=data_user)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Extract data from the response
        data = response.json()
        
        # Return the data
        return data
    except requests.exceptions.RequestException as e:
        # If an error occurs during the request, catch it here
        print('Lỗi khi gọi API:', e)
        
        # Rethrow the error
        raise
    
def saveRequestCost(data_request : any, api_url: any):
    try:
        # Send a POST request to the specified URL with the data
        url = api_url + '/application.service/create-service-cost'
        response = requests.post(url, json=data_request)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Extract data from the response
        data = response.json()
        
        # Return the data
        return data
    except requests.exceptions.RequestException as e:
        # If an error occurs during the request, catch it here
        print('Lỗi khi gọi API:', e)
        
        # Rethrow the error
        raise
