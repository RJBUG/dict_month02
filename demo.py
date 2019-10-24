import getpass
import hashlib

password = getpass.getpass()

print(password)

# 加密处理
hash = hashlib.md5(b'@#$%^&*()_+')
hash.update(b'password')
passwd = hash.hexdigest()
print(passwd)
