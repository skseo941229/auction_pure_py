import requests
import sys
import json
import sys
import sys
from pybp.pederson import PedersonCommitment
from pybp.rangeproof import RangeProof
import zipfile
import pickle
from urllib.request import urlretrieve


url = "http://0.0.0.0:8000"


headers = {
    'Content-Type':'application/json',
}
     
if __name__ == "__main__":
    print("----------Menu----------")
    print("0: Enter the value you want to bid")
    print("1: Place your bid")
    print("2: Open bids. ex) name, h_x, h_y, b (blinding factor)") 
    print("3: Get Winner/Verification") 
    print("4: Finish the bidding program") 
    print("------------------------")
    
    value = 0 
    name = str(sys.argv[1])
    h_x = 0
    h_y = 0
    b = 0
    c_x = 0
    c_y = 0
    
    while True:
        menu = input("Type the menu number you want: ")
        if menu == "4":
            break
        if menu == "0":
            value = input("Type the bid price: ")
            value = int(value)
            rp = RangeProof(32) 
            proofval = value & (2**32 - 1)
            rp.generate_proof(proofval)
            Varg = PedersonCommitment(value, b = rp.gamma)
            h_x, h_y = Varg.h
            b = Varg.b 
            c_x, c_y = Varg.get_commitment()
            print("Your pedersen commitment value is------")
            print("Bid_x: ", c_x)
            print("Bid_y: ", c_y)
        elif menu == "1": 
            check = input("Want to use above pedersen commitment value you have? y/n: ")
            if check == "y":
                data = {'id': name, 'bid_x': str(c_x), 'bid_y':str(c_y)}
                r = requests.post(url+"/bid", data = json.dumps(data), headers=headers).json()
                if r == "0":
                    print("Your bid is placed")
                else:
                    print("You are not allowed to place bid! We already closed the deals")
            else:
                print("Check menu....")
        elif menu == "2":
            check = input("Want to use h and r value you have? y/n: ")
            if check == "y":
                data = {'id': name, 'value':str(value),'h_x': str(h_x), 'h_y':str(h_y), 'b':str(b)}
                r = requests.post(url+"/check", data = json.dumps(data), headers=headers).json()
                print(r)
            else:
                print("Check menu....")
        elif menu == "3":
            print("----Your result-----")
            data = {'id': name}
            r = requests.post(url+"/get_win", data = json.dumps(data), headers=headers).json()
            if r == "You are the winner":
                print(r)
            else:
                print("We received zip file for verification")
                urlretrieve("file:///"+r, 'archive_zipfile-'+ name+'.zip')
            
                with zipfile.ZipFile('archive_zipfile-'+ name+'.zip', 'r') as zip_ref:
                    zip_ref.extractall()

                with open('proof-'+name+'.pickle', 'rb') as handle:
                    proof = pickle.load(handle)
                with open('rp-'+name+'.pickle', 'rb') as handle:
                    rp = pickle.load(handle)
                print("We unzipped files and got 2 files: "+'proof-'+name+'.pickle' + " and "+'rp-'+name+'.pickle' )
                res= rp.verify(proof['Ap'],
                        proof['Sp'],
                        proof['T1p'],
                        proof['T2p'],
                        proof['tau_x'],
                        proof['mu'],
                        proof['t'],
                        proof['proof'],
                        rp.V)
                if res == True:
                    print("You are the loser. Verification is completed")
        

            
            
            
            
            
        