import subprocess
import os
import openai
from openai import OpenAI

# Initialize the OpenAI API Client
# openai.api_key = "YOUR_API_KEY"
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the function that will interact with ChatGPT using a given prompt
def call_gpt(prompt):
    messages = [
        {
            "role": "system",
            "content": "You are a cybersecurity SOC analyst with more than 25 years of experience."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    client = OpenAI()
    response = client.chat.completions.create(
        model = "gpt-4-turbo-preview", 
        messages = messages,
        max_tokens = 2048,
        n=1,
        stop=None,
        temperature=0.7
    )
    response.choices[0].message.content.strip()

# This function will run a given windows command and return the output
def run_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    return result.stdout

# Gather data from key locations on the system
# registry_data = run_command("reg query HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall")
# print(registry_data)

process_data = run_command("tasklist /v")
print(process_data)

network_data = run_command("netstat -an")
print(network_data)

scheduled_tasks = run_command("schtasks /query /fo LIST /v")
print(scheduled_tasks)

security_logs = run_command("wevtutil qe Security /c:10 /rd:true /f:text") #Last 10 security events. Adjust the number as needed
print(security_logs)

# Analyze the data using ChatGPT
analysis_result = call_gpt(f"Analyze the following Windows system data for signs of APTs:\nProcess Data:\n{process_data}\n\nNetwork Data\n{network_data}\n\nScheduled Tasks\n{scheduled_tasks}\n\nSecurity Logs\n{security_logs}")
# add Registry Data:\n{registry_data}\n\n if used

#Display the analysis result
print(f"Analysis Result:\n{analysis_result}")