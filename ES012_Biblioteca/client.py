import requests
import pandas as pd

id = input("ID: ")
if(id == "all"):
    results = requests.get("http://127.0.0.1:5000/api/v1/resources/books/all")
else:
    results = requests.get("http://127.0.0.1:5000/api/v1/resources/books", params={"id":id})

results = eval(results.text)

print(results)

df = pd.DataFrame(results)
print(df)