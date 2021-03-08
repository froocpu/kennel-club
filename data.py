import csv


def prepare_force_simulation_data(doggy_dict: list):
    nodes = [{"id": dog["name"],
              "colour": dog["colour"],
              "sex": dog["sex"],
              "gen": dog["generation"]} for dog in doggy_dict]
    node_ids = [dog['name'] for dog in doggy_dict]
    links = []
    for dog in doggy_dict:
        if dog.get('sire') and dog['sire'] in node_ids:
            links.append({"source": dog["name"], "target": dog["sire"], "value": "sired"})
        if dog.get('dam') and dog['dam'] in node_ids:
            links.append({"source": dog["name"], "target": dog["dam"], "value": "damed"})
    return {"nodes": nodes, "links": links}


def prepare_d3_stratify_data(doggy_list):

    root = [dog for dog in doggy_list if dog["generation"] == 0][0]
    output = [(root["name"], "", root["colour"], root["sex"], root["dob"])]

    for dog in doggy_list:
        # get child for each dog
        children = [i_dog for i_dog in doggy_list if i_dog["name"] in (dog["sire"], dog["dam"])]
        for child in children:
            output.append(
                (child["name"], dog["name"], child["colour"], child["sex"], child["dob"])
            )
    return output


def write_d3_stratify_data(data):
    with open("d3/data.csv", "w") as file_out:
        HEADERS = ["child", "parent", "colour", "sex", "dob"]
        csv_out = csv.writer(file_out)
        csv_out.writerow(HEADERS)
        for i in prepare_d3_stratify_data(data):
            csv_out.writerow(i)
