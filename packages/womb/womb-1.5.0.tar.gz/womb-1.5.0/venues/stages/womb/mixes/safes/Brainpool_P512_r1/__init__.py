

'''
	from womb.mixes.safes.Brainpool_P512_r1 import 
'''


'''
import ecdsa
from ecdsa.curves import NISTCurve, brainpoolP256r1, brainpoolP384r1, brainpoolP512r1

# Select the Brainpool curve you want to use
curve = brainpoolP256r1  # Change to brainpoolP384r1 or brainpoolP512r1 for other curves

# Generate a private key
private_key = ecdsa.SigningKey.generate(curve=curve)

# Derive the public key from the private key
public_key = private_key.get_verifying_key()

# Serialize the public key in compressed and uncompressed formats
public_key_compressed = public_key.to_string("compressed")
public_key_uncompressed = public_key.to_string("uncompressed")

# Sign a message with the private key
message = b"Hello, World!"
signature = private_key.sign(message)

# Verify the signature with the public key
is_valid = public_key.verify(signature, message)

print("Public Key (compressed):", public_key_compressed.hex())
print("Public Key (uncompressed):", public_key_uncompressed.hex())
print("Signature:", signature.hex())
print("Signature Validity:", is_valid)

'''

import ecdsa
from ecdsa.curves import brainpoolP512r1

def generate ():
	curve = brainpoolP512r1
	private_key = ecdsa.SigningKey.generate (curve = curve)
	public_key = private_key.get_verifying_key ()
	
	public_key_compressed = public_key.to_string ("compressed")
	public_key_uncompressed = public_key.to_string ("uncompressed")
	
def sign ():
	return;
	
def verify ():
	return;