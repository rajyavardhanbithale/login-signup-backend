from cryptography.fernet import Fernet

message = "hello geeks"


key = b"K3nYOXKcW7BIVmCYMmrvNKTw5YShzlRtOT-3-qTK4Gk="



fernet = Fernet(key)


encMessage = fernet.encrypt(message.encode())

print("original string: ", message)
print("encrypted string: ", encMessage)

decMessage = fernet.decrypt(encMessage).decode()

print("decrypted string: ", decMessage)
