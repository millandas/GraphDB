from database import neo

def setup_graphs():
    conn = neo.session_handler()
    with conn.session() as sess:
        graph_exists = sess.run("CALL gds.graph.exists('twitter-graph') YIELD exists RETURN exists").single()["exists"]
        if not graph_exists:
            sess.run("CALL gds.graph.project('twitter-graph', 'User', 'FOLLOWS')")

        undirected_exists = sess.run("CALL gds.graph.exists('twitter-graph-undirected') YIELD exists RETURN exists").single()["exists"]
        if not undirected_exists:
            sess.run("""
                CALL gds.graph.project('twitter-graph-undirected', 'User',
                    {FOLLOWS: {orientation: 'UNDIRECTED'}})
            """)
    return {"status": "success", "message": "Graphs initialized"}

def exec_pagerank():
    conn = neo.session_handler()
    with conn.session() as sess:
        data = sess.run("""
            CALL gds.pageRank.stream('twitter-graph')
            YIELD nodeId, score
            RETURN gds.util.asNode(nodeId).username AS username, score
            ORDER BY score DESC LIMIT 10
        """)
        return [r.data() for r in data]

def exec_betweenness():
    conn = neo.session_handler()
    with conn.session() as sess:
        data = sess.run("""
            CALL gds.betweenness.stream('twitter-graph')
            YIELD nodeId, score
            RETURN gds.util.asNode(nodeId).username AS username, score
            ORDER BY score DESC LIMIT 10
        """)
        return [r.data() for r in data]

def exec_degree():
    conn = neo.session_handler()
    with conn.session() as sess:
        data = sess.run("""
            CALL gds.degree.stream('twitter-graph', {orientation: 'REVERSE'})
            YIELD nodeId, score
            RETURN gds.util.asNode(nodeId).username AS username, score AS followers
            ORDER BY score DESC LIMIT 10
        """)
        return [r.data() for r in data]

def exec_community():
    conn = neo.session_handler()
    with conn.session() as sess:
        data = sess.run("""
            CALL gds.louvain.stream('twitter-graph')
            YIELD nodeId, communityId
            RETURN gds.util.asNode(nodeId).username AS username, communityId LIMIT 20
        """)
        return [r.data() for r in data]

def exec_triangles():
    conn = neo.session_handler()
    with conn.session() as sess:
        data = sess.run("""
            CALL gds.triangleCount.stream('twitter-graph-undirected')
            YIELD nodeId, triangleCount
            RETURN gds.util.asNode(nodeId).username AS username, triangleCount
            ORDER BY triangleCount DESC LIMIT 10
        """)
        return [r.data() for r in data]

def exec_path(start, end):
    conn = neo.session_handler()
    with conn.session() as sess:
        start_node = sess.run("MATCH (u:User {username: $username}) RETURN id(u) as id", username=start).single()
        end_node = sess.run("MATCH (u:User {username: $username}) RETURN id(u) as id", username=end).single()

        if not start_node or not end_node:
            return {"error": "User not found"}

        data = sess.run("""
            CALL gds.shortestPath.dijkstra.stream('twitter-graph', {
                sourceNode: $startNode, targetNode: $endNode
            })
            YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
            RETURN index, gds.util.asNode(sourceNode).username AS source,
                gds.util.asNode(targetNode).username AS target, totalCost,
                [nodeId IN nodeIds | gds.util.asNode(nodeId).username] AS nodeNames, costs
        """, startNode=start_node["id"], endNode=end_node["id"])

        return [r.data() for r in data]
