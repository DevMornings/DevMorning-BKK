#Author: busara-s
#Create date: 23/02/25
#Desc: This is fix a keywords search to the most popular repo realted to AI and model

import requests
import ollama

# GitHub API URL (Search AI-related repositories)
API_URL = "https://api.github.com/search/repositories?q=ai+model&sort=stars"

# Send request
response = requests.get(API_URL, headers={"Accept": "application/vnd.github.v3+json"})

# Parse response
if response.status_code == 200:
    data = response.json()
    for repo in data["items"][:5]:  # Show top 5 results
        
        print(f"🔹 {repo['name']} - {repo['html_url']}")
        print(f"⭐ Stars: {repo['stargazers_count']} | 🍴 Forks: {repo['forks_count']}")
        
        #Ask llm to summarize the content
        response = ollama.chat(
            model="llama3.2:1b",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"Summary the key important topics:\n{repo['description']}",
                },
            ],
        )

        # Extract the message content, skip if no description
        if hasattr(response, "message") and response.message.content:
            content = response.message.content
            print(f"📖 Description: {content}\n")
        
        
else:
    print("❌ Error fetching data:", response.status_code)