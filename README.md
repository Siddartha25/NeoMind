# NeoMind🧠: Context-Based Chatbot with Knowledge Graph

Chatbots play a crucial role in modern customer support for businesses. Traditionally, chatbots operated in a rigid, rule-based manner, responding to predefined queries with scripted answers. However, with advancements in Large Language Models (LLMs), organizations are shifting towards more intelligent and dynamic chatbots capable of delivering context-aware, personalized customer interactions.

These next-generation chatbots can retain conversation history and access a database of past resolved queries, allowing them to learn from previous interactions and provide more effective, informed responses. This significantly enhances the overall customer experience, as users receive answers that are not only relevant but also informed by prior interactions and similar past issues.

The Challenge of Leveraging LLMs for Customer Support
Despite their potential, most companies lack the resources to develop their own state-of-the-art LLMs trained specifically on their proprietary data. Instead, they rely on powerful third-party LLMs such as OpenAI’s models or LLaMA for customer support automation. However, a key limitation arises: these general-purpose LLMs are not inherently trained on company-specific knowledge. This leads to gaps in contextual understanding, making them less effective for specialized support tasks.

To overcome this challenge, businesses need a framework that bridges the gap between cutting-edge LLMs and their own domain-specific knowledge, ensuring that the chatbot remains informed and relevant to their unique requirements.

# Introducing NeoMind
NeoMind is designed as a flexible and intuitive framework that enables users to create custom chatbots with ease. The core idea behind NeoMind is to enhance LLM-based chatbots with domain-specific knowledge and a distinct personality to align with the needs of different applications.
![alt text](https://github.com/Siddartha25/NeoMind/blob/main/Neomind.png?raw=true)
## How NeoMind Works
- ### Leveraging Knowledge Graphs for Contextual Understanding
NeoMind utilizes Knowledge Graphs (KGs) to store structured knowledge that the chatbot can reference. This allows for precise context retrieval by finding relevant information based on semantic similarity between incoming user queries and existing knowledge. Instead of relying solely on an LLM’s pre-trained data, NeoMind dynamically supplies contextual information to the model, ensuring more accurate and relevant responses.

- ### Enhancing Responses with Similar Past Queries
One of the most powerful features of NeoMind is its ability to learn from past queries and resolved issues. By storing previous solutions in the form of knowledge, the chatbot can retrieve and reuse information from similar past cases, significantly improving efficiency in handling repetitive or related queries. This makes it particularly useful for customer support, where similar problems frequently arise, and solutions can be automatically suggested based on prior cases.

- ### Customizable Chatbot Personality
NeoMind takes chatbot customization further by allowing users to define a personality for their chatbot. Whether it needs to be formal and professional for enterprise applications or casual and engaging for social interactions, the chatbot’s personality can be tailored to the specific needs of the business.

# Using NeoMind

## 1. Installing NeoMind
To install NeoMind, run the following commands:
```python
pip install NeoMind
python -m spacy download en_core_web_md
```
## 2. Get a Free API Key
To use NeoMind, you need an API key for accessing Groq's language model.
Visit [Groq](https://groq.com/) to sign up and obtain a free API key.

## 3. Create your knowledge graph
NeoMind uses Neo4j for knowledge graphs, you need an URI of an knowledge graph instance for using NeoMind.
Visit [Neo4j Aura](https://neo4j.com/product/auradb/) to sign up and create a new instance and obtain URI.

## 4. Create a chatbot
- Importing 
```python
from NeoMind import Chat, Neo4jHandler
```

- Setting up the knowldge graph and adding knowledge
```python
# Neo4j Database Configuration
NEO4J_URI = ""
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = ""

# Initialize Neo4j Handler
graph_handler = Neo4jHandler(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)

# Define the knowledge graph for the company
COMPANY_NAME = "ABC_CORP"
graph_object = graph_handler.get_or_create_graph(COMPANY_NAME)

# Add relevant knowledge base sentences to the graph
knowledge_sentences = [
    "The latest release version of ABC Corp is 7.1.2, which was released in January 2021.",
    "Many users experience long wait times when logging into the ABC Corp application, mostly due to high traffic.",
    "ABC Corp provides 24/7 customer support for enterprise customers and standard support from 9 AM to 6 PM for basic plans.",
    "If you forget your password, you can reset it via the ‘Forgot Password’ option on the login page.",
    "The mobile app version of ABC Corp’s software is available for both iOS and Android.",
    "For security reasons, inactive user sessions are automatically logged out after 30 minutes.",
    "Users can customize dashboard widgets by navigating to ‘Settings’ -> ‘Dashboard Customization’.",
    "The system supports exporting reports in CSV, PDF, and Excel formats.",
    "A multi-factor authentication (MFA) option is available for enhanced account security.",
    "Users experiencing billing issues should contact billing@abccorp.com for assistance.",
]

# Insert sentences into the knowledge graph
graph_handler.add_sentences_to_graph(COMPANY_NAME, knowledge_sentences)
```
- Setting up the chatbot
 ```python 
# Initialize Chatbot with API Key
GROQ_API_KEY = ""
chat_handler = Chat(GROQ_API_KEY)

# Define chatbot personality
chatbot_personality = [
    "Your name is Alex and you are a professional customer support executive for ABC Corp, a company that provides software solutions for managing customer data.",
    "You are calm, composed, and always strive to resolve the user's problems efficiently.",
    "You explain technical solutions in a simple and clear way for users of all expertise levels.",
    "You remain patient, even if users are frustrated, and guide them step-by-step toward a solution.",
    "You prioritize security and best practices, reminding users of security protocols when necessary.",
    "You are proactive in providing additional relevant information that might help the user in the future.",
    "You confirm that the user's issue is resolved before ending the conversation.",
]

# Set chatbot personality
chat_handler.set_personality(chatbot_personality)
```
- Putting it together
```python
# Interactive Chat Loop
print("\nWelcome to ABC Corp Customer Support Chatbot!")
print("Type your query below (or type 'exit' to quit):\n")

while True:
    user_query = input("User: ")
    
    if user_query.lower() in ["exit", "quit"]:
        print("Exiting chatbot. Have a great day!")
        break

    # Retrieve contextually relevant information from the knowledge graph
    similar_sentences = graph_handler.get_similar_sentences(COMPANY_NAME, user_query, similarity_threshold=0.7)

    # Generate a response using the chatbot
    chatbot_response = chat_handler.chat_with_groq_KG(user_query, similar_sentences)

    print(f"Chatbot: {chatbot_response}\n")

```

## Why NeoMind?
NeoMind offers a smart prompt-engineering approach that combines cutting-edge LLM capabilities with structured knowledge retrieval, making it a powerful and scalable solution for creating intelligent, context-aware, and reliable chatbots. With its ability to integrate knowledge graphs, retrieve similar past queries, and adapt its personality, NeoMind stands out as a practical framework for businesses looking to enhance their automated support and conversational AI solutions.
