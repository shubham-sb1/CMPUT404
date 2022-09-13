import requests
print(f"Request version : {requests.__version__} ")
print( requests.get('http://www.google.com'))
print(requests.get("https://raw.githubusercontent.com/shubham-sb1/CMPUT404/main/labs/lab01/lab.py").text)

