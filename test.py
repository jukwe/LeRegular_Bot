from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from mnemonic import Mnemonic
import base58

# Connect to the Solana network
solana_client = Client("https://api.devnet.solana.com") # https://api.mainnet-beta.solana.com

def create_wallet():
    mnemo = Mnemonic("english")
    my_words = mnemo.generate(256)
    seed_bytes = Bip39SeedGenerator(my_words).Generate()
    bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.SOLANA)
    bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)
    bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)

    # Get the private key bytes from the derived context
    private_key_bytes = bip44_chg_ctx.PrivateKey().Raw().ToBytes()

    # Create a Keypair from the private key bytes
    keypair = Keypair.from_seed(private_key_bytes[:32])
    
    return keypair

def get_account_balance(keypair):
    # Get the public key from the keypair
    account_pubkey = keypair.pubkey()  # Convert the pubkey to a string for the API call

    # Fetch the account balance
    balance_response: GetBalanceResp = solana_client.get_balance(account_pubkey)
    print(balance_response)
    # Check if the request was successful
    if balance_response.value is not None:
        sol_balance = balance_response.value / 10**9  # Convert lamports to SOL
        print(f"Account Balance: {sol_balance} SOL")
    else:
        print("Failed to fetch the account balance.")

keypair = create_wallet()
get_account_balance(keypair)


