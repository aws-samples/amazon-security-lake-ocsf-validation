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

hashcode = "validate.py"
hashtest = "c0a489d7e931ded225b4eadf26ff73574ef7e001a850b016a8acb1018a85999a"
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
