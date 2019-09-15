import logging
import time
import vim

import rpc

logger = logging.getLogger(__name__)
logger.setLevel(20)

START_TIME = int(time.time())

BASE_ACTIVITY = {
    'details': 'Idle',
    'timestamps': {
        'start': START_TIME
     },
    'assets': {
        'large_text': 'The one true editor',
        'large_image': 'neovim'
        # 'small_text': 'The one true editor',
        # 'small_image': 'neovim2'
     }
 }

CLIENT_ID = '622902431029919755'

thumbnails = {
    'js': 'JavaScript',
    'py': 'Python',
    'rs': 'Rust',
    'md': 'Markdown',
    'ts': 'TypeScript',
    'go': 'Go',
    'hs': 'Haskell',
    'json': 'JSON',
    'zig': 'Zig',
}


def get_filename():
    return vim.eval('expand("%:t")')


def get_extension():
    return vim.eval('expand("%:e")')


def get_cwd():
    return vim.eval('getcwd()')


def get_neovim_version():
    return 'todo'


def update_presence(connection):
    if rpc.connection_closed:
        rpc.close(connection)
        logger.error('Connection to Discord closed.')
        return

    activity = BASE_ACTIVITY
    filename = get_filename()
    cwd = get_cwd()
    if not filename or not cwd:
        return

    activity['details'] = 'Editing ' + filename
    activity['assets']['small_text'] = get_neovim_version()

    extension = get_extension()
    if extension and extension in thumbnails.keys():
        activity['assets']['large_image'] = extension
        activity['assets']['large_text'] = \
            'Editing a {} file'.format(thumbnails[extension])
    else:
        activity['assets']['large_image'] = 'neovim'
        activity['assets']['lage_text'] = f'unknown filetype: {extension}'

    try:
        rpc.set_activity(connection, activity)
    except NameError:
        logger.error('Discord is not running!')
    except BrokenPipeError:
        logger.error('Connection to Discord lost!')
