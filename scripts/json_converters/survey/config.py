
types = {"D":"['demographics']", 
         "C":"['current_practice']", 
         "E":"['experience']",
         "EC":"['edge_cases']", 
         "N":"['needs']"}

shared = ["ResponseID"]

ranked = []

multi = ["N1"]

single = ["D1","D2","C5","E1","E3","E5","EC2","EC4","N5"]

ranked_answers = {}

ids = {"in_house":"In-house legal counsel",
       "outside":"Outside legal counsel",
       # "not_practicing":"Not currently engaged in the practice of law",
       "other":"Other (please explain)"}