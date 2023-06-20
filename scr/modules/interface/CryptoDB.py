import os
import shutil
class CryptoDB():

  

    def delete_folder():
        folder_path = 'resources/pricedata'
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            print(f"Der Ordner '{folder_path}' wurde erfolgreich gelöscht.")
        else:
            print(f"Der Ordner '{folder_path}' existiert nicht.")
