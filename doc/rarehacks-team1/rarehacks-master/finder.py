from urllib import request
from urllib.error import HTTPError
import xml.etree.cElementTree as ET


def query(lng, lat, offset=.01):
    print("Running query with coords. {},{}".format(lng, lat))
    hospitals = []
    clinics = []
    worked = False
    while not worked and offset > 0:
        try:
            url = "https://api.openstreetmap.org/api/0.6/map?bbox={},{},{},{}" \
                      .format(round(float(lng) - offset, 4), round(float(lat) - offset, 4),
                              round(float(lng) + offset, 4), round(float(lat) + offset, 4))
            req = request.Request(url)
            response = request.urlopen(req)
            it = ET.fromstring(response.read())
            for node in it.iter("node"):
                for tag in node.iter("tag"):
                    if tag.attrib["k"] == "amenity":
                        if tag.attrib["v"] == "hospital":
                            hospitals.append(node)
                        elif tag.attrib["v"] == "clinic":
                            clinics.append(node)
            worked = True
        except HTTPError as err:
            if err.code == 400:
                offset -= .001
    return hospitals + clinics, offset


def find(lng, lat):
    print("Running finder")
    result, offset = query(lng, lat)
    or_offset = offset
    if len(result) != 0:
        return result
    while len(result) == 0:
        for i_lng in [lng + i * or_offset for i in range(int(-offset/or_offset), int(offset/or_offset))]:
            rang = [lat - offset, lat + offset]
            if i_lng in [lng - offset, lng + offset]:
                rang = [lat + i * or_offset for i in range(int(-offset / or_offset), int(offset / or_offset))]
            for i_lat in rang:
                local_result, _ = query(i_lng, i_lat, or_offset)
                result += local_result
        offset += or_offset
    return result


def get_details(id):
    print("Getting details for id {}".format(id))
    req = request.Request("https://api.openstreetmap.org/api/0.6/node/{}".format(id))
    response = request.urlopen(req)
    it = ET.fromstring(response.read())
    results = dict()
    results["id"] = id
    for tag in it.iter("tag"):
        results[tag.attrib["k"]] = tag.attrib["v"]
    return results


"""
if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)
    lng = float(sys.argv[1])
    lat = float(sys.argv[2])
    nodes = find(lat, lng)
    #for a in [get_details(nodes[i]) for i in range(len(nodes))]:
    for a in nodes:
        print(a)
    #return [get_details(nodes[i].attrib["id"]) for i in range(len(nodes))]
"""