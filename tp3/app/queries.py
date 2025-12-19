from database import neo

def fetch_query(q_id: int):
    conn = neo.session_handler()
    cypher = ""

    if q_id == 1:
        cypher = "MATCH (u:User) RETURN u LIMIT 5"
    elif q_id == 2:
        cypher = "MATCH (u1:User)-[r:FOLLOWS]->(u2:User) RETURN u1.username, type(r), u2.username LIMIT 5"
    elif q_id == 3:
        cypher = "MATCH (t:Tweet) RETURN t.text LIMIT 3"
    elif q_id == 4:
        cypher = "MATCH (t1:Tweet)-[r:RETWEETS]->(t2:Tweet) RETURN t1.id, type(r), t2.id LIMIT 5"
    elif q_id == 5:
        cypher = "MATCH (t:Tweet) WITH count(t) as total, count(t.createdAt) as present RETURN 1.0 - (toFloat(present) / total) as missing_ratio"
    elif q_id == 6:
        cypher = "MATCH ()-[r]->() RETURN type(r) as type, count(r) as count"
    elif q_id == 7:
        cypher = "MATCH (t1:Tweet)-[:RETWEETS]->(t2:Tweet) RETURN t1.text as retweet_text, t2.text as original_text LIMIT 5"
    elif q_id == 8:
        cypher = "MATCH (t:Tweet) WHERE t.createdAt IS NOT NULL RETURN substring(t.createdAt, 0, 4) as year, count(t) as count ORDER BY year"
    elif q_id == 9:
        cypher = "MATCH (t:Tweet) WHERE t.createdAt STARTS WITH '2021' RETURN t.id, t.text, t.createdAt LIMIT 10"
    elif q_id == 10:
        cypher = "MATCH (t:Tweet) WHERE t.createdAt IS NOT NULL RETURN substring(t.createdAt, 0, 10) as day, count(t) as count ORDER BY count DESC LIMIT 5"
    elif q_id == 11:
        cypher = "MATCH (t:Tweet)-[:MENTIONS]->(u:User) WHERE NOT (u)-[:PUBLISH]->(:Tweet) RETURN count(DISTINCT u) as users_mentioned_without_tweets"
    elif q_id == 12:
        cypher = "MATCH (t1:Tweet)-[:RETWEETS]->(t2:Tweet)<-[:PUBLISH]-(u:User) RETURN u.username, count(t1) as retweets_received ORDER BY retweets_received DESC LIMIT 10"
    elif q_id == 13:
        cypher = "MATCH (t:Tweet)-[:MENTIONS]->(u:User) RETURN u.username, count(t) as mentions ORDER BY mentions DESC LIMIT 10"
    elif q_id == 14:
        cypher = "MATCH (u1:User)-[:FOLLOWS]->(u2:User) RETURN u2.username, count(u1) as followers ORDER BY followers DESC LIMIT 10"
    elif q_id == 15:
        cypher = "MATCH (u1:User)-[:FOLLOWS]->(u2:User) RETURN u1.username, count(u2) as following ORDER BY following DESC LIMIT 10"
    else:
        return {"error": "Invalid question ID"}

    with conn.session() as sess:
        data = sess.run(cypher)
        return [r.data() for r in data]
