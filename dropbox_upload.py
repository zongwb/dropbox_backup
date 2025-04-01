"""Dropbox: Upload a local directory"""

import os
import pathlib

import dropbox
import httpx

from settings import settings


class DropboxUtil:
    """A thin wrapper for the Dropbox client"""

    def __init__(self, app_key, app_secret, refresh_token) -> None:
        self.access_token = self.get_access_token(app_key, app_secret, refresh_token)
        with dropbox.Dropbox(oauth2_access_token=self.access_token) as dbx:
            dbx.users_get_current_account()

    @staticmethod
    def get_access_token(app_key, app_secret, refresh_token) -> str:
        """Get the refresh token from Dropbox. This is a long lived token that can be used to get a short lived
        access token, without user interactions."""
        # https://www.codemzy.com/blog/dropbox-long-lived-access-refresh-token#how-can-i-get-a-refresh-token-manually
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        params = {'refresh_token': refresh_token, 'grant_type': 'refresh_token'}
        res = httpx.post(
            'https://api.dropboxapi.com/oauth2/token', auth=(app_key, app_secret), headers=headers, params=params
        )
        return res.json()['access_token']

    @staticmethod
    def local_path_to_dropbox_path(local_path, dirname):
        """Convert the local path to Dropbox path, removing the prefix"""
        dropbox_path = local_path.removeprefix(dirname)
        if not dropbox_path.startswith('/'):
            dropbox_path = '/' + dropbox_path
        return dropbox_path

    def upload_folder(self, folder):
        """Upload a local folder to Dropbox"""
        dirname = os.path.dirname(folder)
        with dropbox.Dropbox(oauth2_access_token=self.access_token) as dbx:
            for root, _, files in os.walk(folder, topdown=False):
                for name in files:
                    file_path = os.path.join(root, name)
                    print(f'Local file  : {file_path}')
                    dropbox_path = self.local_path_to_dropbox_path(file_path, dirname)
                    print(f'Dropbox file: {dropbox_path}')

                    with open(file_path, 'rb') as f:
                        dbx.files_upload(f.read(), dropbox_path, mute=True)

    def rename_folder(self, old_name, new_name):
        """Rename a folder in Dropbox"""
        with dropbox.Dropbox(oauth2_access_token=self.access_token) as dbx:
            dbx.files_move_v2(old_name, new_name)

    def delete_folder(self, folder):
        """Remove a folder in Dropbox"""
        with dropbox.Dropbox(oauth2_access_token=self.access_token) as dbx:
            dbx.files_delete_v2(folder)


def remove_trail_slash(s):
    """ "Remove the ending slash in a path"""
    if s.endswith('/'):
        s = s[:-1]
    return s


def main():
    """Main processing flow"""
    dbc = DropboxUtil(settings.dropbox_app_key, settings.dropbox_app_secret, settings.dropbox_refresh_token)
    local_folder = remove_trail_slash(settings.folder_name)
    basename = pathlib.PurePath(local_folder).name
    try:
        dbc.delete_folder('/' + basename + '.bak')
    except Exception as e:   # pylint: disable=broad-exception-caught
        print(e)

    try:
        dbc.rename_folder('/' + basename, '/' + basename + '.bak')
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(e)

    dbc.upload_folder(local_folder)


if __name__ == '__main__':
    main()
