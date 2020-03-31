#API - https://haveibeenpwned.com/API/v3#PwnedPasswords
#Hash Generator - https://passwordsgenerator.net/sha1-hash-generator/
#reference: https://www.geeksforgeeks.org/sha-in-python/

import requests,hashlib,sys

#Request api data from the pwnedpasswordd
def request_api_data(hash_5):
    url = 'https://api.pwnedpasswords.com/range/' + hash_5
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again!')
    return res

#Creating a database
def database(response):
    response_text = response.text
    dict1 = {}
    for string in response_text.splitlines():
        hashid = string.split(':')[0]
        count = string.split(':')[1]
        dict1[hashid] = count
    return dict1

# d = database(request_api_data('0018A'))
# print(d),type(d)

#check password if it exist in API response
def pwned_api_check(password):
    hash = hashlib.sha1(password.encode()).hexdigest().upper()
    hash_5,hash_gt5 = hash[:5],hash[5:]
    print(hash_5,hash_gt5)
    resp1 = request_api_data(hash_5)
    #Get the dict
    dict1 = database(resp1)
    #Check if the password exist
    if dict1.get(hash_gt5) != None:
        print (f'The password: ${password}$ has been hacked {dict1[hash_gt5]} times')
    else:
        print(f'The password: ${password}$ has never been hacked')
    return("ALl done!")

for password in sys.argv[1:]:   
    sys.exit(pwned_api_check(password))
