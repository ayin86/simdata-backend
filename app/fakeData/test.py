import hashlib
import base64

# 原始字符串
original_string = "password"
last_three_characters = original_string[-3:]

md5_hash = hashlib.md5(original_string.encode()).hexdigest()
base64_encoded = base64.b64encode(last_three_characters.encode()).decode()

print("MD5 Hash:", md5_hash)
print("Base64 Encoded:", base64_encoded)

print(md5_hash+base64_encoded)
# 5f4dcc3b5aa765d61d8327deb882cf99b3Jk
# 5f4dcc3b5aa765d61d8327deb882cf99b3Jk
# 5f4dcc3b5aa765d61d8327deb882cf99

import secrets
secret_key = secrets.token_hex(32) 
print(secret_key)