# यह script ऐसे फोटो हटा देगा जो JSON में तो हैं लेकिन फोल्डर में नहीं हैं।

import os
import json

with open("user_photos.json", "r") as f:
    user_photos = json.load(f)

uploads = os.listdir("static/uploads/")
for user in user_photos:
    user_photos[user] = [photo for photo in user_photos[user] if photo in uploads]

with open("user_photos.json", "w") as f:
    json.dump(user_photos, f, indent=4)
