from serpapi import GoogleSearch

params = {
  "engine": "google_shopping",
  "q": "Geladeira Electrolux",
  "location": "Austin, Texas, United States",
  "hl": "en",
  "gl": "us",
  "api_key": "41f64670fd12a5992c579f36ea06eed6f460e2631302a1d1c947c4fa5584c199"
}

search = GoogleSearch(params)
results = search.get_dict()
shopping_results = results["shopping_results"]