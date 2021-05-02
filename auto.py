import aes

key=os.getenv('key')
js=os.getenv('json')

output=aes.AESCipher(key).encrypt(js)
with open('qmail.txt','w') as f:
  f.write(output)
