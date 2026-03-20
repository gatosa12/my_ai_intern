"""
Retell AI Hello World — verifies SDK auth and lists available agents.
Run: python retellai_hello_world.py
"""
import os
from dotenv import load_dotenv
from retell import Retell

load_dotenv()

api_key = os.getenv("RETELLAI_API_KEY")
if not api_key:
    raise ValueError("RETELLAI_API_KEY not set in .env")

client = Retell(api_key=api_key)

def main():
    print("Connecting to Retell AI...")
    agents = client.agent.list()
    print(f"Success! Your Retell AI connection is working.")
    print(f"Agents on this account: {len(agents)}")
    for agent in agents:
        print(f"  - [{agent.agent_id}] {agent.agent_name}")

if __name__ == "__main__":
    main()
