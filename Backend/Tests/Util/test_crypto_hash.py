from Backend.Util.Crypto_hash import crypto_hash

def test_crypto_hash():
    assert crypto_hash(1,[2],'tres') != crypto_hash('tres',1,[2])
