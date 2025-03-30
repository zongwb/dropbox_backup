# pylint: disable-all
import os

import httpx
import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect


APP_KEY = os.environ['DROPBOX_APP_KEY']
APP_SECRET = os.environ['DROPBOX_APP_SECRET']
REFRESH_TOKEN = os.environ['REFRESH_TOKEN']

# https://www.codemzy.com/blog/dropbox-long-lived-access-refresh-token#how-can-i-get-a-refresh-token-manually
def get_access_token_from_refresh_token(app_key, app_secret, refresh_token):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'refresh_token': refresh_token, 'grant_type': 'refresh_token'}
    res = httpx.post(f'https://api.dropboxapi.com/oauth2/token', auth=(app_key, app_secret),
     headers=headers, params=params)
    return res.json()['access_token']

def upload_dir(dbx, folder):
    # upload extracted images to Dropbox
    for root, dirs, files in os.walk(folder, topdown=False):
        print(f'root {root}')
        for name in files:
            file_path = os.path.join(root, name)
            print(f'file {file_path}')
            
            with open(file_path, "rb") as f:
                dbx.files_upload(f.read(), '/'+file_path, mute=True)



def rename_folder(dbx, old_name, new_name):
    dbx.files_move_v2(old_name, new_name)

def delete_folder(dbx, folder):
    dbx.files_delete_v2(folder)

def main():
    access_token = get_access_token_from_refresh_token(APP_KEY, APP_SECRET, REFRESH_TOKEN)
    with dropbox.Dropbox(oauth2_access_token=access_token) as dbx:
        dbx.users_get_current_account()
        try:
            delete_folder(dbx, '/test.bak')
        except Exception as e:
            print(e)

        try:
            rename_folder(dbx, '/test', '/test.bak')
        except Exception as e:
            print(e)

        upload_dir(dbx, 'test')

if __name__ == '__main__':
    main()
    