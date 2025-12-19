# Social Network Graph Analytics

Neo4j-based Twitter network analytics engine with Graph Data Science capabilities.

## Core Capabilities

### CSV Import Pipeline
- Unique constraints for User/Tweet entities
- Batch CSV ingestion from remote sources
- Relationship mapping: followers, tweets, mentions, retweets, replies
- Optimized for large-scale datasets

### Graph Modeling
- Directed graph structures for algorithm execution
- Undirected variants for pathfinding operations
- Projection management and inspection

### Analytics Suite
- **PageRank**: Rank users by influence and follower importance
- **Betweenness**: Detect bridge accounts connecting network segments
- **Degree**: Track follower/following metrics (in/out-degree)
- **Louvain**: Detect communities via modularity optimization
- **Triangle Count**: Analyze clustering coefficients
- **Dijkstra**: Compute shortest paths between accounts

### Query Interface
- Sample node/edge exploration
- Relationship type statistics
- Temporal tweet distribution analysis
- Influence metrics (followers, mentions, retweets)
- Data completeness validation
- Ghost user detection (mentioned but inactive)

## Data Endpoints

CSV sources loaded via HTTPS:
- Accounts: `https://bit.ly/39JYakC`
- Follow graph: `https://bit.ly/3n08lEL`
- Posts: `https://bit.ly/3y3ODyc`
- User tags: `https://bit.ly/3tINZ6D`
- Repost links: `https://bit.ly/3QyDrRl`
- Reply chains: `https://bit.ly/3b9Wgdx`

## Data Model

**Entities:**
- `User`: Accounts with id, username, name, registeredAt
- `Tweet`: Posts with id, text, createdAt

**Edges:**
- `FOLLOWS`: User → User subscription
- `PUBLISH`: User → Tweet authorship
- `MENTIONS`: Tweet → User tag
- `RETWEETS`: Tweet → Tweet amplification
- `IN_REPLY_TO`: Tweet → Tweet conversation thread

## Query Implementations

All 15 analysis queries implemented:
1. Random user sampling
2. Follow relationship sampling
3. Tweet content sampling
4. Retweet relationship visualization
5. Missing timestamp ratio calculation
6. Relationship type distribution
7. Original vs retweet comparison
8. Annual tweet volume
9. 2021 tweet filtering
10. Peak activity days
11. Tagged but inactive users
12. Most retweeted accounts
13. Most mentioned accounts
14. Highest follower counts
15. Highest following counts

## Technical Notes

- Uses `MERGE` for idempotent imports (prevents duplicates)
- Transaction batching recommended for production scale
- Requires Neo4j GDS plugin installation
- Course assignment implementation
