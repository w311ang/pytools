import aes
import os

key=os.getenv('key')
js=os.getenv('json')

output=aes.AESCipher(key).encrypt(js)
with open('jmail.txt','w') as f:
  f.write(str(output))
