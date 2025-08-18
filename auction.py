name = input("Enter your name: ")
bid = int(input("Enter your bid: $"))
other = input("Are there any other bidders? Type 'yes' or 'no': ").lower()

bids = {}
bids[name] = bid
while other == "yes":
    name = input("Enter your name: ")
    bid = int(input("Enter your bid: $"))
    bids[name] = bid
    other = input("Are there any other bidders? Type 'yes' or 'no': ").lower() == "yes"
highest_bidder = ""
highest_bid = 0
for bidder in bids:
    if bids[bidder] > highest_bid:
        highest_bid = bids[bidder]
        highest_bidder = bidder

print(f"The winner is {highest_bidder} with a bid of ${highest_bid}.")
