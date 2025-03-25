import asyncio
import json
from nats.aio.client import Client as NATS
from config.config import NATS_URL

async def run():
    nc = NATS()
    await nc.connect(servers=[NATS_URL])

    async def vehicle_route_by_date_handler(msg):
        data = json.loads(msg.data.decode())
        plate = data.get("plate", "unknown plate")
        start = data.get("start_date", "unknown")
        end = data.get("end_date", "unknown")
        print(f"[Received] vehicle_route_by_date → plate: {plate}, start: {start}, end: {end}")
        result = f"Vehicle {plate} traveled from İzmir to Muğla between {start} and {end}."
        await msg.respond(result.encode())

    async def shipment_status_by_plate_handler(msg):
        data = json.loads(msg.data.decode())
        plate = data.get("plate", "unknown plate")
        shipment_id = data.get("shipment_id", "unknown")
        print(f"[Received] shipment_status_by_plate → plate: {plate}, shipment_id: {shipment_id}")
        result = f"Shipment {shipment_id} carried by {plate} is currently in Afyon."
        await msg.respond(result.encode())
        
    async def handle_total_distance_by_date(msg):
        data = json.loads(msg.data.decode())
        plate = data.get("plate", "unknown plate")
        start = data.get("start_date", "unknown")
        end = data.get("end_date", "unknown")
        print(f"[Received] total_distance_by_date → plate: {plate}, start: {start}, end: {end}")
        result = f"Vehicle {plate} traveled 500 km between {start} and {end}."
        await msg.respond(result.encode())

    await nc.subscribe("vehicle_route_by_date", cb=vehicle_route_by_date_handler)
    await nc.subscribe("shipment_status_by_plate", cb=shipment_status_by_plate_handler)
    await nc.subscribe("total_distance_by_date", cb=handle_total_distance_by_date)

    print("🟢 NATS test subscriber listening on subjects: vehicle_route_by_date, shipment_status_by_plate ...")
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(run())
