# Sealed bid auction purely based on python

1. **Description**  
Before adopting solidity in auction program, I implemented a purely python based sealed auction.  
This auction program is executed using CLI and composed of three parts: auction, auction_info, and bidders.
- auction starts a auction server and responds to the requests from auction_info and bidders.
- auction_info gives information about the auction such as list of bidders, and permission to close bid.
- bidders can submit the value and check their results. 

In pure python based sealed auction, pedersen commitment and bulletproof were used.
To implement this auction, please install this package first.   
https://github.com/kendricktan/pybp



2. **Implementation**   
Once you implement auction, auction_info, bidder program, CLI gives guidance how to progress auction program.   

Executing the auction: 
```
python auction.py
```

Execute the auction_info:
```
python auction_info.py
```

Execute the bidder:
```
python bidder.py <bidder_name>
```
