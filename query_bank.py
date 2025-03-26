# Central registry of all available query templates in the system.
# Each entry defines the query name, description, required parameters, and corresponding endpoint.
# Used by the router agent to match user intent to a known query type.

QUERY_BANK = [
    {
        "name": "vehicle_route_by_date",
        "description": "Get where a vehicle went in a specific date range.",
        "params": ["plate", "start_date", "end_date"],
        "endpoint": "/vehicle/route"
    },
    {
        "name": "shipment_status_by_plate",
        "description": "Get current shipment status of a specific vehicle.",
        "params": ["plate", "shipment_id"],
        "endpoint": "/shipment/status"
    },
    {
        "name": "total_distance_by_date",
        "description": "Get total distance traveled by a vehicle in a given date range.",
        "params": ["plate", "start_date", "end_date"],
        "endpoint": "/vehicle/distance"
    },
    {
        "name": "current_location_by_plate",
        "description": "Get current location of a specific vehicle.",
        "params": ["plate"],
        "endpoint": "/vehicle/current_location"
    }
]
