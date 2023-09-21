import codecs
import hashlib
import base58
import ecdsa
from bit import Key


def fromZeroToAddress():
    
    private_key=Key()._pk.to_hex()
    private_key_bytes = codecs.decode(private_key, 'hex')
    public_key_raw = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
    public_key_bytes = public_key_raw.to_string()
    public_key_hex = codecs.encode(public_key_bytes, 'hex')
    uncompressed_public_key = (b'04' + public_key_hex).decode("utf-8")
    if (ord(bytearray.fromhex(uncompressed_public_key[-2:])) % 2 == 0):
        public_key_compressed = '02'
    else:
        public_key_compressed = '03'
    public_key_compressed += uncompressed_public_key[2:66]
    
    public_key_compressed = bytearray.fromhex(public_key_compressed)
    public_key_uncompressed=bytearray.fromhex(uncompressed_public_key)

    compressed=fromPubkeyGetAddress(public_key_compressed)
    uncompressed=fromPubkeyGetAddress(public_key_uncompressed)

    return [private_key,compressed,uncompressed]


def fromZeroToAddressFILE():
        
    private_key=Key()._pk.to_hex()
    private_key_bytes = codecs.decode(private_key, 'hex')
    public_key_raw = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
    public_key_bytes = public_key_raw.to_string()
    public_key_hex = codecs.encode(public_key_bytes, 'hex')
    uncompressed_public_key = (b'04' + public_key_hex).decode("utf-8")
    if (ord(bytearray.fromhex(uncompressed_public_key[-2:])) % 2 == 0):
        public_key_compressed = '02'
    else:
        public_key_compressed = '03'
    public_key_compressed += uncompressed_public_key[2:66]
    
    public_key_compressed = bytearray.fromhex(public_key_compressed)
    public_key_uncompressed=bytearray.fromhex(uncompressed_public_key)

    compressed=fromPubkeyGetHash160(public_key_compressed)
    uncompressed=fromPubkeyGetHash160(public_key_uncompressed)

    return [private_key,compressed,uncompressed]


def fromPubkeyGetAddress(k):
    #k should be bytearray.fromhex(public_key)
    sha = hashlib.sha256()
    sha.update(k)
    sha.hexdigest() # .hexdigest() is hex ASCII
    rip = hashlib.new('ripemd160')
    rip.update(sha.digest())
    key_hash = rip.hexdigest()
    modified_key_hash = "00" + key_hash
    key_bytes = codecs.decode(modified_key_hash, 'hex')
    address = base58.b58encode_check(key_bytes)
    if type(address)==bytes: #used to make sure that the output from  walletData is a list of string
        address=address.decode('utf-8')
    return address

def fromPubkeyGetHash160(k):
    #k should be bytearray.fromhex(public_key)
    sha = hashlib.sha256()
    sha.update(k)
    sha.hexdigest() # .hexdigest() is hex ASCII
    rip = hashlib.new('ripemd160')
    rip.update(sha.digest())
    key_hash = rip.hexdigest()
    return key_hash



