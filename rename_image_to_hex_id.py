import os
from uuid import uuid4

UPLOAD_FOLDER = "uploads"

mapping = {}  # to map old name -> new hex id

for filename in os.listdir(UPLOAD_FOLDER):
    old_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.isfile(old_path):
        continue

    # split name and extension
    name, ext = filename.rsplit(".", 1)

    # generate hex id
    image_id = uuid4().hex

    # new filename
    new_filename = f"{image_id}.{ext}"
    new_path = os.path.join(UPLOAD_FOLDER, new_filename)

    # rename file
    os.rename(old_path, new_path)

    # save mapping
    mapping[name] = image_id

#     print(f"{filename}  →  {new_filename}")
#
# print("\nUse this mapping to update your DB:")
# print(mapping)
