# Sealed bid auction purely based on python

This is a first step of a progressive sealed-bid auction.

## Description

In this phase, any blockchain technology was not employed. For hiding a bidding price, pedersen commitment was employed. For verification of losing bids, bulletproof was used. 
- Auction starts a auction server and responds to the requests from auction_info and bidders.
- Auction_info gives information about the auction such as list of bidders, and has a permission to close bid.
- Bidders can submit the value and check their results. 


## Getting Started

### Dependencies

* Ganache

### Installing

* pybp package (https://github.com/kendricktan/pybp)

### Executing program
* Executing the auction: 
```
python auction.py
```

* To query auction status, execute the auction_info:
```
python auction_info.py
```

* To be a bidder of a program, execute the bidder:
```
python bidder.py <bidder_name>
```
