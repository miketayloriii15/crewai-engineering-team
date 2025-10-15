#!/usr/bin/env python3
import os
from engineering_team.crew import EngineeringTeam

from dotenv import load_dotenv
load_dotenv()  # loads .env into os.environ

# Project details
requirements = """
Build a simple ecommerce site for Movies & Books:
- FastAPI backend with /health, /products, /cart, /checkout
- In-memory catalog and cart (no DB)
- Frontend: Bootstrap site with search, filters, cart, and checkout
- Tests for all endpoints
"""
module_name = "shop_backend.py"
class_name = "ShopService"

def run():
    os.makedirs("output", exist_ok=True)
    inputs = {
        "requirements": requirements,
        "module_name": module_name,
        "class_name": class_name,
    }
    result = EngineeringTeam().crew().kickoff(inputs=inputs)
    print("\n=== CREW RUN COMPLETE ===\n")
    print(result)

if __name__ == "__main__":
    run()
