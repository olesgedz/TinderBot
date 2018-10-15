import itertools
import pynder
import config

FBTOKEN = config.FACEBOOK_AUTH_TOKEN

FBID = "100000904101013"

session = pynder.Session(facebook_id=FBID, facebook_token=FBTOKEN)
print(session)
users = session.nearby_users()
for i in users:
    print(i)

print(helllllll)
