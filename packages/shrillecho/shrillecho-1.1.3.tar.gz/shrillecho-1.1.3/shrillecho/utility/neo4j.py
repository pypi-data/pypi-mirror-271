from typing import List
from neo4j import GraphDatabase

from shrillecho.types.artist_types import Artist

uri = "bolt://localhost:7687"
username = "neo4j"
password = "Zxasqw12"

driver = GraphDatabase.driver(uri, auth=(username, password))

def create_and_relate_artist(main_artist, other_artists):

    def create_and_relate_artists(tx, main_artist: Artist, other_artists: List[Artist]):
    
        main_artist_query = "MERGE (main:Artist {name: $main_artist}) RETURN main"
        tx.run(main_artist_query, main_artist=main_artist.name)
        
        for artist in other_artists:
            # For each artist in the list, create or find the artist node and create a RELATED_TO relationship
            artist_query = """
            MERGE (other:Artist {name: $artist})
            WITH other
            MATCH (main:Artist {name: $main_artist})
            MERGE (main)-[:RELATED_TO]->(other)
            """
            tx.run(artist_query, main_artist=main_artist.name, artist=artist.name)


    with driver.session() as session:
        session.execute_write(create_and_relate_artists, main_artist, other_artists)  
   