import requests

endpoints='http://127.0.0.1:8000/car/list/'

get_response=requests.get(endpoints)
print(get_response.json(),get_response.status_code)