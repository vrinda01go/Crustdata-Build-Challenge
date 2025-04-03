import requests

s = requests.Session()


res1 = s.post("http://localhost:8000/interact", json={"command": "search for big bang theory series on wikipedia"})
print("Step 1:", res1.json())

# Step 2: Get reviews (uses stored topic)
res2 = s.post("http://localhost:8000/interact", json={"command": "get reviews"})
print("Step 2:", res2.json())

res3 = s.post("http://localhost:8000/interact", json={"command": "where can i see it"})
print("Step 3:", res3.json())