from web3 import Web3
import requests
import sys
import json

web3 = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/9850c004bcc64e57b914fd5617af1621"))
url = "http://0.0.0.0:8000"

headers = {
    'Content-Type':'application/json',
}

if __name__ == "__main__":
    print("----------Menu----------")
    print("1: List current bidding")
    print("2: Finalize auction") 
    print("3: Print open bids")
    print("4: Announce Winner") 
    print("5: Finish the auction program") 
    print("------------------------") 
    
    while True:
        menu = input("Type the menu number you want: ")
        if menu == "5":
            break      
        if menu == "1": 
            data = requests.get(url+"/list").json()
            print("Now, there are "+ str(len(data))+" bidders!")
            print("Name".ljust(8) , "bid_x".ljust(10) , "bid_y".ljust(10)) 
            for item in data:
                print(item['id'].ljust(8),     item['bid_x'].ljust(10),item['bid_y'].ljust(10)) 
        elif menu == "2":
            data = requests.get(url+"/close") 
            print("Closed the auction")
        elif menu == "3":
            r = requests.get(url+"/open_list").json()
            print("Name".ljust(10), "Price")
            for item in r:
                print(item.ljust(10),r[item])
        elif menu == "4":
            r = requests.post(url+'/get_win', data=json.dumps({'id':"owner"}), headers=headers).json()
            print(r)