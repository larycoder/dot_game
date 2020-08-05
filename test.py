import base64
encoded = base64.b64encode(b'hello world').decode()
decoded = base64.b64decode(encoded)

myString = "hello world"
myByte = bytes(myString, 'utf-8')
print(myByte)

# from dot_game import db
# print(db.session.bind.url.database.split("/")[-1])

myDict = dict(
    x = 'hello',
    y = 'ok'
)

print(myDict)
