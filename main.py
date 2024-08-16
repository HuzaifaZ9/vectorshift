from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import networkx as nx

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",  # React frontend
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Node(BaseModel):
    id: str

class Edge(BaseModel):
    source: str
    target: str

class Pipeline(BaseModel):
    nodes: list[Node]
    edges: list[Edge]

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

@app.post('/pipelines/parse')
async def parse_pipeline(pipeline: Pipeline):
    num_nodes = len(pipeline.nodes)
    num_edges = len(pipeline.edges)
    
    graph = nx.DiGraph()
    for node in pipeline.nodes:
        graph.add_node(node.id)
    for edge in pipeline.edges:
        graph.add_edge(edge.source, edge.target)
    
    is_dag = nx.is_directed_acyclic_graph(graph)
    
    return {"num_nodes": num_nodes, "num_edges": num_edges, "is_dag": is_dag}
