from math import floor
import os
import sys
from requests import get
import certifi
import threading
import time
import threading
import tracemalloc
import generateBtcWallet


MULTIPLE_ADDRESS_ENDPOINT = {
    "name1": ["url", 1],
    "name": ["url", 1,],
    "name": ["url", 1,]
}


def parse_url(endpoint: str, addressList):
    """
    This, composes the url for the request to the endpoint.
    With given endpoint (prefix), it append the all the addresses in addressList.
    @return the endpoint well formed
    """
    
    first = True
    for i, address in enumerate(addressList):
        if first:
            first = False
        else:
            endpoint += ","
        endpoint += address
        
    return endpoint


def get_balance(
    provider: str, addressList, recursive=False):
    """
    Given the provider (see MULTIPLE_ADDRESS_ENDPOINT to check the available provider), a list of wallet addresses, check the balance of all provided addresses.
    The parameter recursive is used to make another requests if the first return status code different from 200.
    """
    endpoint=MULTIPLE_ADDRESS_ENDPOINT.get(provider)[0]
    endpointUrl = parse_url(endpoint, addressList)
    try:
        response = get(endpointUrl, timeout=10, verify=pathCertificate)
        if response.status_code != 200:
            print(
                "Status code response: "
                + str(response.status_code)
                + " from "
                + provider
            )
            time.sleep(5)
            if not recursive:
                print("Recursive with " + provider)
                return get_balance(provider, addressList, True)
            return [0, False]

        response = response.json()
        balance = switch(provider, response, addressList)
        return balance

    except Exception as e:
        print("Exception on get_balance with " + provider + ": ", e)
        return [0, False]


def switch(provider: str, json, addressList):
    """
    Given the endpoint provider (see MULTIPLE_ADDRESS_ENDPOINT), the json response, and the addresses list, it try to find the balance of each address in the json response
    @return the list of all balance and a bool to verify if there are some balance greater then zero.
    """
    balance = []
    found=False

    #if provider == "name1":
        #check balance....
        #if balance>0:
            #balance.append(currentBalance)
            #found=True


    return [balance,found]


def createWalletListFromZero(nAddress):
    """
    This allows to create a list with specified size where the elements are the pair (private_key,public_key)
    @return a list with the pair 
    """
    walletsList = []
    for _ in range(nAddress):
        walletData = generateBtcWallet.fromZeroToAddress()
        if type(walletData[1])==bytes: #used to make sure that the output from  walletData is a list of string
            walletData[1]=walletData[1].decode()
        if type(walletData[2])==bytes: #used to make sure that the output from  walletData is a list of string
            walletData[2]=walletData[1].decode()
        #[0]: private_key ; [1]: public address compressed ; [2] public address uncompressed 
        walletsList.append(walletData)
    return walletsList


def task(provider: str):
    """
    The main of the script where generate the addresses, check the balance and if there is positive balance. If successful writes to a file the private key and the address
    """
    global count
    nAddress=floor(MULTIPLE_ADDRESS_ENDPOINT.get(provider)[1]/2)
    while True:
        
        walletsList=createWalletListFromZero(nAddress)
        addressList = []
        for i in range(len(walletsList)):
            addressList.append(walletsList[i][1])
            addressList.append(walletsList[i][2])
        balanceList = get_balance(provider, addressList)
        if balanceList[1]:
            print("Balance list:")
            print(balanceList)
            print("Wallet list:")
            print(walletsList)
            f=open("found_with_multiple_addresses.csv", "a")
            for i, balance in enumerate(balanceList[0]): #int 116
                if balance != -1 and balance != 0.00000000000000000:
                    f.write(
                        str(balance)
                        + ","
                        + walletsList[i][1]
                        + ","
                        + walletsList[i][2]
                        + ","
                        + walletsList[i][0]
                        + "\n"
                        )
            f.close()
        with threadLock:
            count += nAddress
        

def restart():
    """
    It restart the script.
    Function used before to solve memory leak.
    """
    print("RESTART")
    if sys.platform=="Linux": #Change if you have different PATH
        os.execv("/usr/bin/python3",["python3"]+["/home/ubuntu/bruteforce-wallet-balance/multithreading_multiple_address.py"])
    os.execv(sys.executable, ['python'] + sys.argv)



#---------------------------MODIFY----------------------------------

nThread = 3 #Here, you can set how many endpoint check. Value higher then size of MULTIPLE_ADDRESS_ENDPOINT items does nothing. Example: You can specify it with 1 to check at the same time two endpoint.
timeoutDisplayInfo=60
#-------------------------------------------------------------------

pathCertificate = certifi.where()
count = 0 #sum of addresses checked
previousCount=0
threadLock = threading.Lock()
start = time.time()
time.sleep(1)
tracemalloc.start()

for i, threadNumber in enumerate(MULTIPLE_ADDRESS_ENDPOINT.items()):
    if i == nThread:
        break
    thread = threading.Thread(
        target=task, args=([threadNumber[0]])
    )
    print(
        "Start thread "
        + str(i)
        + " with "
        + threadNumber[0]
        + " and url "
        + threadNumber[1][0]
        + " and  max address "
        + str(threadNumber[1][1])
    )
    thread.start()

while True:
    print("Processed " + str(count)+" addresses")
    partial = time.time()
    print("Elapsed " + str(int(partial - start)) + " seconds from start")
    print("Global mean address checked in one second: " + str(round(count / (partial - start),1)))
    print("60 seconds mean address checked in one second: " + str(round((count-previousCount) / timeoutDisplayInfo,1)))
    print("Current memory usage (in MB):",str(round(tracemalloc.get_traced_memory()[0]/1024/1024,2)))
    print()
    previousCount=count
    time.sleep(timeoutDisplayInfo)

    #Used with old method to solve RAM leak
    #if tracemalloc.get_traced_memory()[0]>350*1024*1024:
    #    print("Memory usage exceeded 350MB")
    #    restart()
    






