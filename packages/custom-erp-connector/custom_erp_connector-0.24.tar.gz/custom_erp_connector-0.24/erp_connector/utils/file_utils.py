import os
import zipfile


def zip_folder(folder_path, zip_path, zip_name):
    zip_path = os.path.join(zip_path, zip_name)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                zipf.write(file_path, arcname=file_name)
    return zip_path
