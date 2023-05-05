# !/usr/bin/env python3
# -*- coding: utf-8 -*-
 
 
import hashlib
import os
import shutil

def get_checksum(filename, hash_function):

    hash_function = hash_function.lower()
 
    with open(filename, "rb") as f:
        bytes = f.read()  # read file as bytes
        if hash_function == "sha256":
            readable_hash = hashlib.sha256(bytes).hexdigest()
        else:
            Raise("{} is an invalid hash function. Please Enter MD5 or SHA256")
 
    return readable_hash

hashcode = "checksum/hash.tar.gz"
hashtest = "59869db34853933b239f1e2219cf7d431da006aa919635478511fabbfc8849d2"
sha256_result = get_checksum(hashcode, "sha256")

print(sha256_result)
print(hashtest)

# If hashes are equal, no error is detected
if str(sha256_result) == str(hashtest):
    print("Checksums are equal.")
    print("STATUS: ACCEPTED")
     
# Otherwise, Error is detected
else:
    print("Checksums are not equal.")
    print("STATUS: ERROR DETECTED")

shutil.rmtree("checksum")
