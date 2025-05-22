import os
import json

UPLOAD_FOLDER = 'static/uploads'
USER_PHOTO_DB = 'user_photos.json'

# User uploads जो वेबसाइट पे दिख रहे हैं
if os.path.exists(USER_PHOTO_DB):
    with open(USER_PHOTO_DB, 'r') as f:
        user_photos = json.load(f)
else:
    user_photos = {}

# सभी इस्तेमाल में आ रही photos को collect करो
used_photos = set()
for photo_list in user_photos.values():
    used_photos.update(photo_list)

# Uploads folder में सभी फाइलें लो
all_files = set(os.listdir(UPLOAD_FOLDER))

# अनयूज़्ड फाइल्स निकालो
unused_files = all_files - used_photos

# Delete unused files
for file in unused_files:
    file_path = os.path.join(UPLOAD_FOLDER, file)
    try:
        os.remove(file_path)
        print(f"Deleted unused file: {file}")
    except Exception as e:
        print(f"Failed to delete {file}: {e}")

print("Cleanup complete.")
