# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!! Needs Chia DevTools & SpaceScan API Key !!!!!!
# !! https://github.com/Chia-Network/chia-dev-tools  !!
# !!!!!!!!!!!!!!! https://spacescan.io !!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# Update the held list "nfts.txt" with current grep of wallet
# Add held list to hash table
# Compare changes between existing unclaimed file
# Output difference to new buys -> this is drop list for 40k
# Overwrite old unclaimed with new unclaimed
# Compare new unclaimed against all nfts list
# If nft from all nfts not in unclaimed -> this is 2k drops list (bi-monthly)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !! new_buys.txt, drop.txt and unclaimed.txt will be overwritten !!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

from time import sleep
from chia.util.bech32m import encode_puzzle_hash, decode_puzzle_hash
import requests

# List of all minted NFT ids
# You will to have either saved these beforehand
# Or get them from the spacescan api or other means
all_nfts = 'Okra_Folk_500.txt'

# List of currently own held NFTs
# Can be gotten with: 
# chia wallet nft list -f 487473619 -i 2 | grep "NFT identifier" | grep -v "nft1fjzg....gqyyzm3w" | cut -d ":" -f 2 | tr -d " \t" >nfts.txt
held_list = 'nfts.txt'

# Unclaimed will be written here
unclaimed = "unclaimed.txt"

held_table = {}
nft_drop_ids = []
new_buy_ids = []

header = {'x-auth-id': '***********ADD API KEY HERE**************'}
nft_info = requests.Session()


def ss_api_request(nft_id, output_file):
    nft_rtn = requests.get(
        url=('https://api2.spacescan.io/v0.1/xch/nft/' + nft_id),
        headers=header)
    nft_json = nft_rtn.json().get('history')
    addr = encode_puzzle_hash(bytes.fromhex(nft_json[0].get("extra_info")), 'xch')
    print("API REQUEST FOR:", nft_id)
    output_file.write(addr + "\n")
    sleep(1)


input(" Begin? Old files with be over written and updated"
      "\n Be sure to gotten the new buys before continuing!\n")
input(" Press Any Key To Confirm Start\n")

# Load hashtable with held for comparisons
with open(held_list, 'r') as file:
    for line in file:
        held_table[line.strip()] = 1

# Write new purchases to new_buys.txt
with open(unclaimed, 'r') as file:
    for line in file:
        if held_table.get(line.strip()) is None:
            new_buy_ids.append(line.strip())

# Updated unclaimed list and add claimed to drop list
unclaimed = open("unclaimed.txt", 'w')

with open(all_nfts, 'r') as file:
    for line in file:
        if held_table.get(line.strip()) == 1:
            unclaimed.write(line)
        else:
            nft_drop_ids.append(line.strip())
unclaimed.close()

# Process drop list and new buys list
# get the current holding address for the nft ids


# Newly bought NFT Addresses
new_buys = open('new_buys.txt', 'w')
for nft in new_buy_ids:
    ss_api_request(nft, new_buys)
new_buys.close()

# Addresses of all distributed NFTs *Also will contain new buys
drop_list = open('drop.txt', 'w')
for nft in nft_drop_ids:
    ss_api_request(nft, drop_list)
drop_list.close()

print("\n\n FINISHED!")
