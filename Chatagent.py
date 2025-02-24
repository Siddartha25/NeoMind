from groq import Groq

class Chat:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.personality = ""
        self.knowledge=""
        self.conversation_history = [
            {
                "role": "system",
                "content": self.personality
            }
        ]
    
    def clear_conversation_history(self):
        #clears chat history but not personlity or knowledge
        self.conversation_history = [
            {
                "role": "system",
                "content": "Your personality is : "+self.personality+". The knowledge that you have is: "+self.knowledge
            }
        ]

    def clear_knowledge(self):
        #clears knowledge but not the personality
        self.knowledge=""
        self.conversation_history[0]["content"]="Your personality is : "+self.personality+". The knowledge that you have is: "+self.knowledge

    def set_personality(self, personality): #used to set personality for the bot
        self.personality=""
        self.knowledge=""  #resetting the knowledge as the personality is changed as knowledge might not be relevant
        for p in personality:
            self.personality += p
        self.conversation_history[0]["content"] = "Your personality is : "+self.personality

    def add_knowledge(self, sentences): #used to add knowledge to the bot
        for sentence in sentences:
            self.knowledge+=sentence
        self.conversation_history[0]["content"]="Your personality is : "+self.personality+". The knowledge that you have is: "+self.knowledge
 
    def chat_with_groq(self,query):
        """Handles conversation memory and returns chatbot response."""
        
        # Append the user's message to the history
        self.conversation_history.append({"role": "user", "content": query})

        # Call the API with the full conversation history
        completion = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=self.conversation_history,  # Pass entire history
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
        )
        response = completion.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": response})
        return response

    def chat_with_groq_KG(self,query,sentences):
        """"this also takes similar sentences from knowledge graph and passes to the chatbot"""
        self.add_knowledge(sentences)
        self.conversation_history.append({"role": "user", "content": query})

        completion = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=self.conversation_history,  # Pass entire history
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
        )
        response = completion.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": response})
        return response
