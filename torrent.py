import hashlib
import bencode
import requests
import socket

#reading the file.
torrentfile = open('ubuntu.torrent', 'rb')
bencodeText = torrentfile.read()
#decoding the bencode
bencodeobject = bencode.decode(bencodeText)
#announce URL, for time sake only http
announceUrl = bencodeobject["announce"]
#finding the infohash from the decoded bencode object
info = bencode.encode(bencodeobject["info"])
infohash = hashlib.sha1(info)
hexstring = infohash.digest()
#sending the request to the tracker and decoding the bencoded response.
parameters = {"info_hash":hexstring, "peer_id":"ejahekskdhaldhsldhwe", "port" : 6303, "uploaded" : 0, "downloaded":0, "left": 23411, "compact" : 1}
response = requests.get(announceUrl, params=parameters)
trackerResponse = response.content
bencodeResponse = bencode.decode(trackerResponse)
#creating array of ip and port number of the peers.
peers = bencodeResponse["peers"]
peerList = []
i = 0
for i in range(0, len(peers), 6):
    ip = socket.inet_ntoa(peers[i:i+4])
    port = int.from_bytes(peers[i+4: i+6], byteorder="big", signed=False)
    item = {"ip":ip, "port": port}
    peerList.append(item)

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

for i in range(0, len(peerList)):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = (peerList[i]["ip"],peerList[i]["port"])
    s.connect(addr)
    s.close() 
    print(i)
     
