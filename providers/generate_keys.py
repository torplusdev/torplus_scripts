# This scripts generates a new stellar account

from stellar_sdk import Keypair


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    keypair = Keypair.random()

    print("Public Key: " + keypair.public_key)
    print("Secret Seed: " + keypair.secret)
    print("-------------------------------------------------------------")
    print("Please make sure to save both your secret seed and the public key.")
    print("If required, public key can be calculated from seed - but the secret seed can not be recovered, "
          "if lost. Please make sure to store it in a safe location")
