import requests
import json

def read_data():
    with open('data.json', 'r') as data_file:
        data = json.load(data_file)

    return data

def verify_code():
    with open('out.txt', 'r') as code:
        data = code.read()
        return data

class CodeRequest:
    def __init__(self, model="codellama"):
        self.model = model
        self.url = "http://localhost:11434/api/chat"
        self.history = [{
            "role": "system",
            "content": f"Only generate the code needed to perform the task the user asking for. If not possible simply reply nothing (empty string). Only return code without any explanation and comments. Make sure to adjust your response to the known user information: {read_data()}"
        }]

    def ask(self, prompt):
        self.history.append({"role": "user", "content": prompt})
        response = requests.post(self.url, json={
            "model": self.model,
            "messages": self.history,
            "stream": False
        })
        message = response.json()["message"]["content"]
        self.history.append({"role": "assistant", "content": message})
        return message
    

class CodeVerifier:
    def __init__(self, model="codellama"):
        self.model = model
        self.url = "http://localhost:11434/api/chat"
        self.history = [{
            "role": "system",
            "content": f"Your task is to verify the code provide along side the instructions of what the code was supposed to do. If correct: Return only the Code! If something wrong: Fix the code and again only return the code! Dont print anything else (no comments or explanations). Make sure to adjust your response to the known user information: {read_data()}"
        }]

    def ask(self, prompt):
        self.history.append({"role": "user", "content": prompt})
        response = requests.post(self.url, json={
            "model": self.model,
            "messages": self.history,
            "stream": False
        })
        message = response.json()["message"]["content"]
        self.history.append({"role": "assistant", "content": message})
        return message


chat = CodeRequest()
verify = CodeVerifier()


while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    
    reply = chat.ask(user_input)

    print("Model:", reply)

    with open('out.txt','w') as file:
        file.write(reply)

    reply = verify.ask(verify_code())

    with open('verified.txt','w') as file:
        file.write(reply)


