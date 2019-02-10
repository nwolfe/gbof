import os
import dropbox

EXE_FILE = 'bindingoffenrir.exe'
DROPBOX_PATH = '/bindingoffenrir.exe'
CHUNKSIZE = 4 * 1024 * 1024  # 4.194304MB

client = dropbox.Dropbox(os.getenv('DROPBOX_TOKEN'))


def upload_in_chunks(file):
    filesize = os.path.getsize(file.name)
    start = client.files_upload_session_start(file.read(CHUNKSIZE))
    cursor = dropbox.files.UploadSessionCursor(start.session_id, f.tell())
    commit = dropbox.files.CommitInfo(
        path=DROPBOX_PATH, mode=dropbox.files.WriteMode.overwrite)
    while file.tell() < filesize:
        if (filesize - f.tell()) <= CHUNKSIZE:
            client.files_upload_session_finish(
                f.read(CHUNKSIZE), cursor, commit)
        else:
            client.files_upload_session_append_v2(
                file.read(CHUNKSIZE), cursor)
            cursor.offset = f.tell()


with open(os.path.join(os.getcwd(), 'dist', EXE_FILE), 'rb') as f:
    upload_in_chunks(f)
