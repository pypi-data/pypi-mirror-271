import requests

def make_request():
    response = requests.get('https://app.tea.xyz')
    return response.text