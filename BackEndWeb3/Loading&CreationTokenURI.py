import requests
import json
import sys

##########################
# VARIABLES DECLARATIONS #
##########################

_TokenName = str(sys.argv[1])
_baseURI = "https://ipfs.infura.io/ipfs/"
_websiteLink = "www.google.com"
_carFile = "immagine.jpg"
_description = "A unique car generated from the Crypto Novus Racing Project!"
#HERE STORE ALL THE PROPERTIES OF THE CAR PIECES! REMEMBER TO ADD AT THE END OF THE FILE
_properties = []




######################################################################################
# IMAGE IPFS UPLOAD API REQUEST AND RETRIEVE THE HASH TO BE INJECTED IN BASEURI+HASH #
######################################################################################

#this _file should be the full built car img OR 3dModel
_file = {
    'file': open(_carFile,'rb')
}

response = requests.post('https://ipfs.infura.io:5001/api/v0/add', files = _file)
p = response.json()
_hash = p['Hash']
print(_hash)


##################################################
# JSON CREATION USING THE METADATA ERC721 SCHEMA #
##################################################

#full json data dict
jsondata = {}

jsondata['name'] = _TokenName
jsondata['description'] = _description
jsondata['image'] = _baseURI+_hash
jsondata['external_url'] = _websiteLink

#the dictionary for the nested json if you want to add attributes to this NFT
_properties = {}

_properties['skin'] = 'Red Skull'
_properties['spoiler'] = 'type 3'
_properties['wheel rim'] = 'type 9'
_properties['vehicle body'] = 'type 10'

#create the full json data file
jsondata['properties'] = _properties


print(json.dumps(jsondata, indent=4))
#write to file
with open('file.json', 'w') as outfile:
    json.dump(jsondata, outfile)



###################################################################################################
# ADD THE FULL JSON FILE AND RETRIVE THE LINK FOR THE MINT->TOKENURI METHOD IN THE SMART CONTRACT #
###################################################################################################

#retrieve the json file
_file = {
    'file': open('file.json','rb')
}

response = requests.post('https://ipfs.infura.io:5001/api/v0/add', files = _file)
p = response.json()
_hash = p['Hash']
print(_hash)

#create the tokenURI link
_tokenURILink = _baseURI+_hash

print(_tokenURILink)
sys.exit(_tokenURILink)