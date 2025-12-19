from fastapi import FastAPI
from database import neo
from loader import import_csv_data
from gds import setup_graphs, exec_pagerank, exec_betweenness, exec_degree, exec_community, exec_triangles, exec_path
from queries import fetch_query

api = FastAPI()

@api.on_event("startup")
def init_db():
    neo.init()

@api.on_event("shutdown")
def close_db():
    neo.cleanup()

@api.get("/")
def root():
    return {"message": "Twitter Network Analysis API"}

@api.post("/load-data")
def init_data():
    return import_csv_data()

@api.post("/create-projections")
def init_graphs():
    return setup_graphs()

@api.get("/analysis/pagerank")
def fetch_pagerank():
    return exec_pagerank()

@api.get("/analysis/betweenness")
def fetch_betweenness():
    return exec_betweenness()

@api.get("/analysis/degree")
def fetch_degree():
    return exec_degree()

@api.get("/analysis/louvain")
def fetch_community():
    return exec_community()

@api.get("/analysis/triangle-count")
def fetch_triangles():
    return exec_triangles()

@api.get("/analysis/shortest-path")
def fetch_path(start_user: str, end_user: str):
    return exec_path(start_user, end_user)

@api.get("/questions/{question_id}")
def fetch_question(question_id: int):
    return fetch_query(question_id)
