import requests

def athiva():

    category = 'happiness'
    api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
    response = requests.get(api_url, headers={'X-Api-Key': '0P00ShHwaZ+t1TnNWLQPTw==oiKhXE2uVXltcuz0'})
    if response.status_code == requests.codes.ok:
        print(response.text)
        return response.text
    else:
        return 'Error' 