import requests
import sys

def walk(rest_hostname, rest_port, rest_username, rest_password, id, direction, indent=0):
    r = requests.get("http://%s:%d/xosapi/v1/core/serviceinstances/%d" % (rest_hostname, rest_port, id), auth=(rest_username, rest_password))
    assert(r.status_code == 200)
    obj = r.json()
    print " "* indent, obj["leaf_model_name"], obj["id"]

    indent = indent+ 4

    if direction=="right":
        for link_id in obj["subscribed_links_ids"]:
            print " "*indent, "link", link_id
            r = requests.get("http://%s:%d/xosapi/v1/core/serviceinstancelinks/%d" % (rest_hostname, rest_port, link_id), auth=(rest_username, rest_password))
            assert(r.status_code == 200)
            link = r.json()
            walk(rest_hostname, rest_port, rest_username, rest_password, link["provider_service_instance_id"], direction, indent+4)
            
    if direction=="left":
        for link_id in obj["provided_links_ids"]:
            print " "*indent, "link", link_id
            r = requests.get("http://%s:%d/xosapi/v1/core/serviceinstancelinks/%d" % (rest_hostname, rest_port, link_id), auth=(rest_username, rest_password))
            assert(r.status_code == 200)
            link = r.json()
            walk(rest_hostname, rest_port, rest_username, rest_password, link["subscriber_service_instance_id"], direction, indent+4)

def main():
    if len(sys.argv)<7:
        print "syntax: walk_service_chain.py <rest_hostname> <rest_port> <rest_username> <rest_password> <service-instance-id> [left | right]"
        sys.exit(-1)

    rest_hostname = sys.argv[1]
    rest_port = int(sys.argv[2])
    rest_username = sys.argv[3]
    rest_password = sys.argv[4]
    id = int(sys.argv[5])
    direction = sys.argv[6]

    walk(rest_hostname, rest_port, rest_username, rest_password, id, direction)

if __name__ == "__main__":
    main()
