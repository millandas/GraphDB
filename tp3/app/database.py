import os
from neo4j import GraphDatabase

class Neo4jConn:
    def __init__(self):
        self.endpoint = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.username = os.getenv("NEO4J_USER", "neo4j")
        self.pwd = os.getenv("NEO4J_PASSWORD", "password")
        self.conn = None

    def init(self):
        self.conn = GraphDatabase.driver(self.endpoint, auth=(self.username, self.pwd))

    def cleanup(self):
        if self.conn:
            self.conn.close()

    def session_handler(self):
        if not self.conn:
            self.init()
        return self.conn

neo = Neo4jConn()
