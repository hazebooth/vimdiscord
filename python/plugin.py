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
        'large_image': 'neovim',
        # 'small_text': 'The one true editor',
        # 'small_image': 'neovim',
     }
 }

CLIENT_ID = '622902431029919755'

thumbnails = {
    'js': 'javascript',
    'py': 'python',
    'rs': 'rust',
    'md': 'markdown',
    'ts': 'typescript',
    'go': 'go',
    'hs': 'haskell',
    'json': 'json',
    'zig': 'zig',
}


def get_filename():
    return vim.eval('expand("%:t")')


def get_relative_file_path():
    return vim.eval('expand("%")')


def get_extension():
    return vim.eval('expand("%:e")')


def get_cwd():
    return vim.eval('getcwd()')


def get_neovim_version():
    return vim.eval("matchstr(execute('version'), 'NVIM v\\zs[^\\n]*')")


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
    # /Users/haze/src/zig-toml

    activity['details'] = 'Editing ' + filename
    project_name = cwd.split('/')[-1]
    activity['details'] = f'Working on {project_name}'

    version = get_neovim_version()
    if version:
        activity['assets']['small_text'] = get_neovim_version()
        activity['assets']['small_image'] = 'neovim'

    activity['assets']['large_text'] = get_relative_file_path()

    extension = get_extension()
    if extension and extension in thumbnails.keys():
        activity['assets']['large_image'] = thumbnails[extension]
    else:
        activity['assets']['large_image'] = 'neovim'

    try:
        rpc.set_activity(connection, activity)
    except NameError:
        logger.error('Discord is not running!')
    except BrokenPipeError:
        logger.error('Connection to Discord lost!')
