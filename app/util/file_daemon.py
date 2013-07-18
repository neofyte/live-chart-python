#original version from http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html
#This script watches the directory and reports the changed filename in the directory.
#modified for this project

import os

import win32file
import win32con

import data_factory

ACTIONS = {
    1 : "Created",
    2 : "Deleted",
    3 : "Updated",
    4 : "Renamed from something",
    5 : "Renamed to something"
}
# Thanks to Claudio Grondi for the correct set of numbers
FILE_LIST_DIRECTORY = 0x0001

APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PATH_TO_WATCH = os.path.join(APP_PATH, 'data\\csv')

hDir = win32file.CreateFile (
    PATH_TO_WATCH,
    FILE_LIST_DIRECTORY,
    win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
    None,
    win32con.OPEN_EXISTING,
    win32con.FILE_FLAG_BACKUP_SEMANTICS,
    None
)


while True:

    data_trans = {}

    #
    # ReadDirectoryChangesW takes a previously-created
    # handle to a directory, a buffer size for results,
    # a flag to indicate whether to watch subtrees and
    # a filter of what changes to notify.
    #
    # NB Tim Juchcinski reports that he needed to up
    # the buffer size to be sure of picking up all
    # events when a large number of files were
    # deleted at once.
    #
    # modified:
    #     delete the unneccessary FILE_NOTIFY_CHANGE'S
    results = win32file.ReadDirectoryChangesW (
        hDir,
        1024,
        True,
         #win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
         #win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
         #win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
         #win32con.FILE_NOTIFY_CHANGE_SIZE |
         win32con.FILE_NOTIFY_CHANGE_LAST_WRITE,# |
         #win32con.FILE_NOTIFY_CHANGE_SECURITY,
        None,
        None
    )

    for action, file_name in results:
        file_path = os.path.join(PATH_TO_WATCH, file_name)
        data_trans['file_name'] = data_factory.database_writer(file_name=file_name, file_path=file_path)
        data_trans['file_name'].db_writer()
        print (file_name, action)

    del data_trans