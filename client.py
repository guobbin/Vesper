import sys, requests


def redirectToLeader(server_address, message):
    type = message["type"]
    # looping until someone tells he is the leader
    while True:
        # switching between "get" and "put"
        if type == "get":
            try:
                response = requests.get(server_address,
                                        json=message,
                                        timeout=1)
            except Exception as e:
                return e
        elif type == "put":
            try:
                response = requests.put(server_address,
                                        json=message,
                                        timeout=1)
            except Exception as e:
                return e
        else:
            try:
                response = requests.delete(server_address,
                                        json=message,
                                        timeout=1)
            except Exception as e:
                return e

        # if valid response and an address in the "message" section in reply
        # redirect server_address to the potential leader
        if response.status_code == 200 and "payload" in response.json():
            payload = response.json()["payload"]
            if "message" in payload:
                server_address = payload["message"] + "/request"
            else:
                break
        else:
            break
    # if type == "get":
    return response.json()
    # else:
    #     return response


# client put request
def put(addr, key, value):
    server_address = addr + "/request"
    payload = {'op': 'put', 'key': key, 'value': value}
    message = {"type": "put", "payload": payload}
    # redirecting till we find the leader, in case of request during election
    print(redirectToLeader(server_address, message))


# client get request
def get(addr, key):
    server_address = addr + "/request"
    payload = {'op': 'get', 'key': key}
    message = {"type": "get", "payload": payload}
    # redirecting till we find the leader, in case of request during election
    print(redirectToLeader(server_address, message))


def delete(addr, key):
    server_address = addr + "/request"
    payload = {'op': 'delete', 'key': key}
    message = {"type": "delete", "payload": payload}
    # redirecting till we find the leader, in case of request during election
    print(redirectToLeader(server_address, message))


def printHow():
    print("PUT usage: python client.py address add 'key' 'value'")
    print("GET usage: python client.py address get 'key'")
    print("DELETE usage: python client.py address del 'key'")
    print("Format: address: http://ip:port")


if __name__ == "__main__":
    if len(sys.argv) == 4:
        # addr, key
        # get
        addr = sys.argv[1]
        op = sys.argv[2]
        key = sys.argv[3]
        if op == 'get':
            get(addr, key)
        elif op == 'del':
            delete(addr, key)
        else:
            printHow()
            # pass
    elif len(sys.argv) == 5:
        # addr, key value
        # put
        if sys.argv[2] == 'put':
            addr = sys.argv[1]
            key = sys.argv[3]
            val = sys.argv[4]
            put(addr, key, val)
        else:
            printHow()
    else:
        printHow()


