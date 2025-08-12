from fastapi import FastAPI
from pydantic import BaseModel
import  chromadb
from sentence_transformers import SentenceTransformer
from typing import List
import uvicorn

#client foleder
embedder = SentenceTransformer("all-MiniLM-L6-v2")

#khalenha aala localhost badal ma heya client bas yaany elhaga mo2kata
#bardo dol f elclient folder 
client = chromadb.EphemeralClient()   #fe 2 clients EphemeralClient w PersistentClient
#EphemeralClient save online w memory not disk law afalt kolo beyde3
#PersistentClient save aala eldisk w loh path mo3ayan law afalt beyfdal mawgod aady mesh beyde3


#da felrepo *
collection = client.get_or_create_collection("cars")













#hansetakhdem pypdf aashan nekhod input w baadeha ltext baadeha n embed ba
docs = [
    "The Toyota Camry is a reliable midsize sedan with good fuel economy and comfortable seating for five.",
    "Ford Mustang is an iconic American muscle car with powerful V8 engine options and sporty design.",
    "Tesla Model 3 is a fully electric vehicle with autopilot features and a minimalist interior design.",
    "Honda Civic is a compact car known for its reliability, fuel efficiency, and affordable maintenance.",
    "Jeep Wrangler is a rugged off-road SUV with removable doors and roof, perfect for adventure seekers.",
    "BMW 3 Series is a luxury sports sedan with precise handling and premium interior materials.",
    "Toyota Prius is a hybrid electric vehicle famous for its exceptional fuel efficiency and eco-friendliness.",
    "Porsche 911 is a high-performance sports car with rear-engine design and distinctive styling.",
    "Ford F-150 is America's best-selling pickup truck, known for its towing capacity and durability.",
    "Volkswagen Golf is a practical hatchback with European styling and fun-to-drive characteristics.",
    "Chevrolet Corvette is an American sports car with mid-engine design and supercar performance.",
    "Subaru Outback is a wagon with all-wheel drive, ideal for outdoor enthusiasts and rough weather conditions.",
    "Mercedes-Benz S-Class is a full-size luxury sedan with cutting-edge technology and plush interiors.",
    "Toyota RAV4 is a popular compact SUV offering a good balance of space, efficiency, and reliability.",
    "Hyundai Tucson is a stylish compact SUV with modern features and a competitive warranty."
]


#repo folder
collection.add(
    documents=docs,
    embeddings=embedder.encode(docs).tolist(),
    ids=[f"id_{i}" for i in range(len(docs))]
)


app = FastAPI(title="Semantic Search API")

#repo  *
class SearchRequest(BaseModel):
    query: str
    top_k: int
#repo   *
class SearchResult(BaseModel):
    results: List[str]


#da haythat f elconroller folder
@app.post("/search", response_model=SearchResult)
def search(request: SearchRequest):# da ba services *
    query_embedding = embedder.encode(request.query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=request.top_k
    )
    for i in results:
        print(i)
        print("-"*20)

    return SearchResult(results=results["documents"][0]) #de ba mmkn ne3tebrha genration bas mafesh llm bas heya betedy info hewl baddeha ba mafrod el llm ezawed kalam based on the info


