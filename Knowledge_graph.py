from neo4j import GraphDatabase
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load spaCy model for sentence embeddings
nlp = spacy.load("en_core_web_md")

class Neo4jHandler:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """ Closes the connection """
        self.driver.close()

    def graph_exists(self, graph_name):
        """Checks if a graph with the given name exists in the Neo4j database"""
        query = """
        MATCH (g:Graph {name: $graph_name})
        RETURN COUNT(g) AS count
        """
        with self.driver.session() as session:
            result = session.run(query, graph_name=graph_name)
            count = result.single()["count"]
        
        return count > 0  # Returns True if graph exists, False otherwise


    def get_or_create_graph(self, graph_name):
        """Checks if a graph with the given name exists; if not, creates one and returns it."""
        query = """
        MERGE (g:Graph {name: $graph_name})
        RETURN g
        """
        with self.driver.session() as session:
            result = session.run(query, graph_name=graph_name)
            graph = result.single()
        return graph

    def add_sentences_to_graph(self, graph_name, sentences):
        """Adds an array of sentences to the specified graph if not exists creates it"""
        self.get_or_create_graph(graph_name)  # Ensure the graph exists first
        for sentence in sentences:
            query = """
            MATCH (g:Graph {name: $graph_name})
            MERGE (s:Sentence {text: $sentence})
            MERGE (s)-[:BELONGS_TO]->(g)
            """
        with self.driver.session() as session:
            for sentence in sentences:
                session.execute_write(lambda tx: tx.run(query, sentence=sentence, graph_name=graph_name))
        print(f"Added {len(sentences)} sentences to the graph '{graph_name}'!")

    def get_all_sentences(self, graph_name):
        """Retrieves all sentences from the specified graph."""
        query = """
        MATCH (s:Sentence)-[:BELONGS_TO]->(:Graph {name: $graph_name})
        RETURN s.text AS sentence
        """
        with self.driver.session() as session:
            result = session.run(query, graph_name=graph_name)
            sentences = [record["sentence"] for record in result]

        if not sentences:
            print(f"No sentences found in graph '{graph_name}'.")
        return sentences

    def get_similar_sentences(self, graph_name, input_sentence, threshold=0.8):
        """Returns an array of sentences from the specified graph that are similar to the input sentence.
        Uses cosine similarity on sentence embeddings.
        """
        query = """
        MATCH (s:Sentence)-[:BELONGS_TO]->(:Graph {name: $graph_name})
        RETURN s.text AS sentence
        """
        with self.driver.session() as session:
            result = session.run(query, graph_name=graph_name)
            sentences = [record["sentence"] for record in result]

        if not sentences:
            print(f"No sentences found in graph '{graph_name}'.")
            return []

        # Compute embeddings
        input_vec = nlp(input_sentence).vector.reshape(1, -1)
        sentence_vectors = [nlp(sent).vector.reshape(1, -1) for sent in sentences]

        # Compute cosine similarity
        similarities = [cosine_similarity(input_vec, sent_vec)[0][0] for sent_vec in sentence_vectors]

        # Filter sentences with similarity above the threshold
        similar_sentences = [sentences[i] for i in range(len(sentences)) if similarities[i] >= threshold]
        return similar_sentences
    
    def delete_all_sentences_in_graph(self, graph_name):
        """Deletes all sentences a specific graph. """

        query = """
        MATCH (s:Sentence)-[:BELONGS_TO]->(g:Graph {name: $graph_name})
        DETACH DELETE s
        """
        with self.driver.session() as session:
            session.run(query, graph_name=graph_name)
        print(f"All sentences in the graph '{graph_name}' have been deleted.")

    def delete_specific_sentences_in_graph(self, graph_name, sentences):
        """Deletes specific sentences within a specific graph."""
        
        query = """
        MATCH (s:Sentence)-[:BELONGS_TO]->(g:Graph {name: $graph_name})
        WHERE s.text IN $sentences
        DETACH DELETE s
        """
        with self.driver.session() as session:
            session.run(query, graph_name=graph_name, sentences=sentences)
        print(f"Deleted {len(sentences)} sentences from the graph '{graph_name}'.")
