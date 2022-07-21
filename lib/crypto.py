import eth_keys, os

#https://eth-account.readthedocs.io/en/stable/eth_account.html#eth_account.account.Account.from_key
#https://cryptobook.nakov.com/digital-signatures/ecdsa-sign-verify-examples

def create_key_pair():
    PrivKey = eth_keys.keys.PrivateKey(os.urandom(32))
    PubKey = PrivKey.public_key
    Address = PubKey.to_checksum_address()
    return (PrivKey,PubKey,Address)

def sign_message(msg,privkey):

    privkey = eth_keys.datatypes.PrivateKey(bytes.fromhex(privkey[2:])) 
    signature = privkey.sign_msg(str.encode(msg))
    return signature

def verify_sign(msg,sign):
    sign = eth_keys.datatypes.Signature(bytes.fromhex(sign[2:])) 
    recoveredPubKey = sign.recover_public_key_from_msg(str.encode(msg))
    return recoveredPubKey

pr = create_key_pair()

print(sign_message('hi','0x2ceadea21c1a23afea0073faf22b2a17c8cc44ecfedef0e2bc7a3281c9c23d8b'))


print('Verified:')
print('0x21a2a2b1376776bbd0eae0f0e82770380c05f62b933c4d9f88e8a5bbe6ae620ebf61389033e586e057388509e96fae74c852dbd63989864a91ae8af566da623c'==str(verify_sign('hi','0x568e2c067b48a30eef91b52756fa88ffeb1e006a20b4a26adcdb339321a258c923f67a51f9af652dda5f4f3f2266f0a50e3658fe100f983bdf79eeec6c1f78a100')))