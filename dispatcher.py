# Sends query requests to the correct backend service via NATS messaging.
# Looks up the target subject based on the query name and publishes a message with extracted parameters.

import asyncio
import json
from nats.aio.client import Client as NATS
from query_bank import QUERY_BANK
from config.config import NATS_URL

async def dispatch_query_nats(routing_result: dict) -> str:
    """
    Sends routing info via NATS to the correct subject (based on query_name),
    awaits response, and returns the result.
    """
    query_name = routing_result.get("query_name")
    if not query_name:
        return "Missing query_name from routing result."

    # Check if query is in the bank
    query_def = next((q for q in QUERY_BANK if q["name"] == query_name), None)
    if not query_def:
        return f"Unknown query name: {query_name}"

    # Prepare payload
    payload = {
        key: routing_result.get(key) for key in query_def["params"]
    }

    try:
        nc = NATS()
        await nc.connect(servers=[NATS_URL])

        # Send request
        msg = await nc.request(
            subject=query_name,
            payload=json.dumps(payload).encode(),
            timeout=5
        )

        await nc.drain()

        return msg.data.decode()

    except Exception as e:
        return f"NATS dispatch error: {str(e)}"
