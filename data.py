

def prepare_nodes_and_links(doggy_dict: list):
    nodes = [{"id": dog['link'],
              "label": dog["name"],
              "colour": dog["colour"],
              "sex": dog["sex"]} for dog in doggy_dict]
    node_ids = [dog['link'] for dog in doggy_dict]
    links = []
    for dog in doggy_dict:
        if dog.get('sire') and dog['sire'] in node_ids:
            links.append({"source": dog["link"], "target": dog["sire"], "value": "sired"})
        if dog.get('dam') and dog['dam'] in node_ids:
            links.append({"source": dog["link"], "target": dog["dam"], "value": "damed"})
    return {"nodes": nodes, "links": links}


def prepare_hierarchy(doggy_dict: list):
    pass