from database import neo

def import_csv_data():
    conn = neo.session_handler()
    with conn.session() as sess:
        sess.run("CREATE CONSTRAINT user_id IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE")
        sess.run("CREATE CONSTRAINT tweet_id IF NOT EXISTS FOR (t:Tweet) REQUIRE t.id IS UNIQUE")

        sess.run("""
            LOAD CSV WITH HEADERS FROM 'https://bit.ly/39JYakC' AS row
            MERGE (u:User {id: row.id})
            SET u.username = row.username, u.name = row.name, u.registeredAt = row.registeredAt
        """)

        sess.run("""
            LOAD CSV WITH HEADERS FROM 'https://bit.ly/3y3ODyc' AS row
            MERGE (t:Tweet {id: row.id})
            SET t.text = row.text, t.createdAt = row.createdAt
        """)

        sess.run("""
            LOAD CSV WITH HEADERS FROM 'https://bit.ly/3y3ODyc' AS row
            MATCH (u:User {id: row.authorId}), (t:Tweet {id: row.id})
            MERGE (u)-[:PUBLISH]->(t)
        """)

        sess.run("""
            LOAD CSV WITH HEADERS FROM 'https://bit.ly/3n08lEL' AS row
            MATCH (u1:User {id: row.source}), (u2:User {id: row.target})
            MERGE (u1)-[:FOLLOWS]->(u2)
        """)

        sess.run("""
            LOAD CSV WITH HEADERS FROM 'https://bit.ly/3tINZ6D' AS row
            MATCH (t:Tweet {id: row.tweetId}), (u:User {id: row.userId})
            MERGE (t)-[:MENTIONS]->(u)
        """)

        sess.run("""
            LOAD CSV WITH HEADERS FROM 'https://bit.ly/3QyDrRl' AS row
            MATCH (t1:Tweet {id: row.source}), (t2:Tweet {id: row.target})
            MERGE (t1)-[:RETWEETS]->(t2)
        """)

        sess.run("""
            LOAD CSV WITH HEADERS FROM 'https://bit.ly/3b9Wgdx' AS row
            MATCH (t1:Tweet {id: row.source}), (t2:Tweet {id: row.target})
            MERGE (t1)-[:IN_REPLY_TO]->(t2)
        """)

        return {"status": "success", "message": "Import complete"}
