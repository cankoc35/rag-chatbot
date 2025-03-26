from query_bank import QUERY_BANK

def get_all_params():
    all_params = set()
    for q in QUERY_BANK:
        all_params.update(q["params"])
    return list(all_params)