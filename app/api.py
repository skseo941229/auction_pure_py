from csv import DictWriter
import json
from unittest import async_case
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import sys
from pybp.pederson import PedersonCommitment
from pybp.rangeproof import RangeProof
from fastapi.responses import  FileResponse
import pickle
import zipfile
import os
import time
import asyncio

app = FastAPI()  

origins = [
    "http://localhost:3000",  
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
bids = []
price = {}
close = "0"

@app.post("/bid", tags=["bids"])  
async def add_bids(bid: dict) -> str:
    '''
    add bid. format receive id, bid_x, bid_y (pedersen commitment is applied)
    
    '''
    if close == "0":
        bids.append(bid)  
        return "0"
    else:
        return str(close)


@app.get("/close", tags=["closing"])    
async def close_bids() -> str:
    global close
    close = "1"
    return "Not accept anymore"  

@app.post("/check")
async def check_bids(pcval:dict) -> str: 
    '''
    receive r, h, value and check that bidders don't lie 
    '''
    global close
    if close =="0":
        return "Not closed anymore"
    if len(bids) ==0:
        return "Nothing in bids"
    
    computedPC = 0
    for bid in bids:
        if bid['id'] == pcval['id']:
            computedPC = PedersonCommitment(int(pcval['value']), b=int(pcval['b']), h=(int(pcval['h_x']), int(pcval['h_y']))).get_commitment()
            if int(bid['bid_x']) == computedPC[0] and int(bid['bid_y']) == computedPC[1]:
                price[bid['id']] = int(pcval['value']) 
                return "Confirmed"
            else:
                bids.remove(bid)    
                return "You are not allowed to participate"  

@app.post("/get_win") 
async def get_winner(id:dict):
    '''
    if winning bid, notify you are the winner. if losing bid, send proof to verify that you are not winner 
    '''
    win_bid = max(price.values())
    for idx in price:
        if price[idx] == win_bid:
            win_idx = idx
            break  

    if win_idx == id['id']:
        return "You are the winner"
    
    if  id['id'] =="owner":
        return str(win_idx+" is the winner")
    
    bid_price = price[id['id']]  
    diff_price = win_bid - bid_price
    proofval = int(diff_price)
    rp = RangeProof(32)
    rp.generate_proof(proofval)
    proof = rp.get_proof_dict()  
    
    with open('proof-'+id['id']+'.pickle', 'wb') as handle:
        pickle.dump(proof, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('rp-'+id['id']+'.pickle', 'wb') as handle:
        pickle.dump(rp, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with zipfile.ZipFile('archive_zipfile-'+ id['id']+'.zip', 'w') as zf:
        zf.write('proof.pickle', compress_type =zipfile.ZIP_DEFLATED)
        zf.write('rp.pickle', compress_type =zipfile.ZIP_DEFLATED)
    zf.close()
    
    return str(os.getcwd()+'/archive_zipfile.zip')
       
@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your Auction list."}

@app.get("/list")
async def list_bidders() -> dict:
    return bids

@app.get("/open_list")
async def open_list() -> dict:
    return price 