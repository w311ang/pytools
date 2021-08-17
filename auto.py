import aes
import os
import json

key=os.getenv('key')
qpass=os.getenv('qpass')
qfrom=os.getenv('qfrom')
js=json.dumps({'qfrom':qfrom,'qpass':qpass})

output=aes.AESCipher(key).encrypt(js)
with open('jmail.txt','w') as f:
  f.write(output.decode("utf-8"))
