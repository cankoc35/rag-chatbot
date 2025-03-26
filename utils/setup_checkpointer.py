import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config import DB_URI
from langgraph.checkpoint.postgres import PostgresSaver

if __name__ == "__main__":
    # Ensure that PostgresSaver is correctly instantiated
    checkpointer = PostgresSaver.from_conn_string(DB_URI)
    with checkpointer as cp:
        cp.setup()
    print("✅ Checkpointer tables created in Postgres.")