import os
import json

UPLOAD_FOLDER = 'static/uploads'
USER_PHOTO_DB = 'user_photos.json'

if os.path.exists(USER_PHOTO_DB):
    with open(USER_PHOTO_DB, 'r') as f:
        user_photos = json.load(f)
else:
    user_photos = {}

changed = False

for user, photos in user_photos.items():
    original = list(photos)
    user_photos[user] = [photo for photo in photos if os.path.exists(os.path.join(UPLOAD_FOLDER, photo))]
    if user_photos[user] != original:
        changed = True

if changed:
    with open(USER_PHOTO_DB, 'w') as f:
        json.dump(user_photos, f, indent=4)
    print("Updated user_photos.json with existing images only.")
else:
    print("No changes needed. All photo references are valid.")
