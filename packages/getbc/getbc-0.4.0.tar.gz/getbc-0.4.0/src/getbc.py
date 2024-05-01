#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 22:14:14 2024
@author: Kenneth E. Carlton

This script file is written in the computer language called python.  This
script's primary purpose is to install the program called bomcheckgui onto your
local computer.  Bomcheckgui compares side-by-side CAD BOMs to ERP BOMs.  For
this program to work you must have a python interpreter prorgram loaded on your
computer.  E.g. https://www.python.org/.

To run this script, open a MS cmd prompt window in the directory where getbc.py
resides and enter this command:

    py getbc.py
"""
__version__ = '0.4.0'
__author__ = 'Kenneth E. Carlton'

#import pdb # use with pdb.set_trace()
import  argparse, webbrowser, os
import sys
from pathlib import Path
import requests
import glob
try:
    from PyQt5.QtWidgets import QApplication
except:
    pass


def get_version():
    return __version__

try:
    fileName = Path(__file__).stem
except:
    fileName = 'getbc'


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                        description=
                        "This program's primary purpose is to install bomcheckgui "
                        "to your local PC, though it can also be used to activate "
                        "bomcheckgui's virtual environment, upgrade to the latest "
                        "version of bomcheckgui, etc.  To install "
                        "bomcheckgui do: py " + fileName +  ".py --install."
                        " (without the period).  Note that before any of getbc's "
                        'commands makes any changes to your computer, '
                        'an explanation will be given about what it is about '
                        'to occur, and then pause and ask for your confirmation '
                        'before proceeding.')
    parser.add_argument('-mh', '--morehelp', action='store_true', default=False,
                        help="More help about using getbc"),
    parser.add_argument('-a', '--about', action='version',
                        version="Author: " + __author__ +
                        ".  Initial creation: Mar 7, 2024.  "
                        + fileName + "'s version no.: " + __version__,
                        help="Show author, creation date, and version, then exit"),
    parser.add_argument('-c', '--copy', action='store_true', default=False,
                        help = 'copy to clipboard: ' + str(activate)),
    parser.add_argument('--install', action='store_true', default=False,
                        help='Create a virtual environment named ' + venvname +
                        ' and install bomcheckgui and bomcheck into it; and ' +
                       'create a link to bomcheckgui on the desktop'),
    parser.add_argument('--uninstall', action='store_true', default=False,
                        help='Uninstall bomcheckgui and bomcheck (will delete ' +
                        'all traces of bomcheckgui, including the bc-venv folder that ' +
                        'contained these scripts.)'),
    parser.add_argument('--upgrade', action='store_true', default=False,
                        help='Show the currently installed software versions and '
                        'show the latest available software versions.  Upgrade '
                        'to newer versions if newer versions are availabe.'),
    parser.add_argument('-v', '--version', action='version', version=__version__,
                        help="Show " + fileName + "'s version number and exit")

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    getbc(vars(args))  # vars() method returns the __dict__ attribute of args


def getbc(dic):
    ''' central hub that calls functions '''
    global flag
    if not sys.platform == 'win32':
        flag = False
        print("This program works only on a MS Windows' OS, and with a regular type of python\n"
              'installation instead of, for example, a python installation like Anaconda\n\n')
    if dic.get('morehelp', False):
        morehelp()
    elif dic.get('copy', False):
        copy()
    elif dic.get('install', False):
        install()
    elif dic.get('uninstall', False):
        uninstall()
    elif dic.get('upgrade', False):
        upgrade()


def morehelp():
    print('Opening browser to show help located on the web...')
    version = 'master'
    bomcheck_help = ('https://htmlpreview.github.io/?https://github.com/'
             'kcarlton55/getbc/blob/' + version + '/help_files/getbc_help.html')
    webbrowser.open(bomcheck_help)


def copy():
    if not Path.exists(activate):
        print('\nA virtual environment is not yet set up.  To set one up enter:\n\n' +
              fileName + ' --install')
        return
    try:
        cb.setText(str(activate), mode=cb.Clipboard)
        print('\nPaste the below to activate a virtual environment.  To deactivate, type: \n'
              'deactivate.  When activated your command prompt will look someting like: \n'
              '(bc-venv) c:\\dir1\\dir2>\n')
        print('This has been copied to the clipboard:\n ' + str(activate))
    except:
        print()
        print('Copy and paste the below to activate a virtual environment.  To deactivate, type: \n'
              'deactivate.  When activated your command prompt will look something like: \n'
              '(bc-venv) c:\\dir1\\dir2>\n')
        print(activate)


def install():
    create_bc_venv = 'py -m venv ' + str(venvpathname)
    activatevenv =  str(activate)
    upgradepip = 'py -m pip install --upgrade pip'
    installbomcheckgui = 'py -m pip install bomcheckgui'
    createdesktoplink = 'mklink /h "' + str(linkto) + '" "' + str(linkfrom) + '"'     # https://www.geeksforgeeks.org/creating-symbolic-links-on-windows/
    print('\nYou are about to install bomcheckgui.  Five commands will be executed.\n'
          'The end result is that you will have a link on your desktop to bomcheckgui:\n\n'

          '1) ' + str(create_bc_venv) +'\n'
          '2) ' + str(activatevenv) + '\n'
          '3) ' + str(upgradepip) + '\n'
          '4) ' + str(installbomcheckgui) + '\n'
          '5) ' + str(createdesktoplink) + '\n\n'

          '1)  The first will create a virtual environment, i.e. a special directory named \n    '
               + str(venvpathname) + '\\.  Bomcheckgui and its dependencies will be\n' +
          '    installed there.\n'
          '2)  The second will make that virtual environment active.  If you were to enter\n'
          '    this command manually, you would see your command prompt change from \n'
          '    something like C:\\users\\John> to (' + venvname + ') C:\\users\\John>.  \n'
          '    With ' + venvname + ' active, packages installed in steps 3 and 4 will \n'
          '    automatically be stored in the ' + venvname + ' folder.\n'
          "3)  The third upgrades pip, python's package manager, to its latest version.\n"
          '    When you first installed python on your computer, pip was automatically\n'
          "    installed.  Pip's function will be to download bomcheckgui from its home\n"
          '    at https://pypi.org/ and install it on your computer.\n'
          '4)  The fourth will install bomcheckgui, along with any dependencies including\n'
          '    bomcheck, into the currently active virtual environment (' + venvname + ').\n'
          '5)  Create a link to bomcheckgui on your deskop.\n'
        )

    if not Path.exists(venvpathname) and not Path.exists(Path(linkto)) and flag:
        x = input('Execute commands (takes a couple of minutes). Continue? (Y/N) ')
        if x.lower().strip()[0] == 'y':
            print('working...')
            command = (create_bc_venv + ' && ' +
                       activatevenv + ' && ' +
                       upgradepip +  ' && ' +
                       installbomcheckgui + ' && ' +
                       createdesktoplink + ' && ' +
                       'echo All 5 of 5 commands executed successfully')
            os.system(command)
            if Path.exists(Path(linkto)):
                print('\nA link has been added to your desktop to run bomcheckgui\n')
            print('If you would like to run bomcheck or bomcheckgui from the cmd console')
            print('do: py ' + fileName + '.py -c')
    elif not flag:
        print('You are not running a MS OS.  No action will be taken')
    else:
        print('Virtual directory and/or desktop link already exists.  No action will be taken.')

def uninstall():
    ''' refence:
    https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/rmdir
    '''
    delete_bc_venv= 'rmdir ' + str(venvpathname) + ' /s /q'
    delete_dektop_bomcheckgui = 'del "' + str(linkto) + '"'
    local_app_folder = os.getenv('LOCALAPPDATA')
    config_folder = os.path.join(local_app_folder, 'bomcheck')
    delete_config_folder = 'rmdir ' + str(config_folder) + ' /s /q'

    print('\nYou are about to uninstall bomcheck, bomcheckgui, their virtual environment,\n'
          'and the bomcheckgui link from your desktop.\n\n'

          '1) ' + delete_dektop_bomcheckgui + '\n'
          '2) ' + delete_bc_venv + '\n'
          '3) ' + delete_config_folder + '\n\n'

          '1) Delete the desktop link to bomcheckgui.exe\n'
          '2) Delete the folder named bc-venv and all its contents.  This will delete\n'
          "   bomcheckgui, bomcheck, and their virtual environment named bc-venv.\n"
          '3) Delete the file named config.txt and the folder in which it resides.\n'
          '   config.txt contains user settings genterated from bomcheckgui.\n\n'

          'If any of these commands does not succeed due to non-existant paths, etc., an\n'
          'error message that you can ignore will show.\n')

    if flag:
        x = input('Execute commands (can take about a minute). Continue? (Y/N) ')
        print()
        if x.lower().strip()[0] == 'y':
            print('working...')
            os.system(delete_dektop_bomcheckgui)
            os.system(delete_bc_venv)
            os.system(delete_config_folder)
    else:
        print('You are not running a MS OS.  No action will be taken.')


def upgrade():
    ''' Upgrade getbc, bomcheck, and bomcheckgui to the latest versions.
    '''
    # dictionary of commands and explanaton of those commands.
    dic = {'getbc':  ['py -m pip install --upgrade ' + fileName,
                     'Upgrade ' + fileName + ' to the latest version.\n'
                     '(' + fileName + 'is located in the base environment.)'],
           'activt': [str(activate),
                     'Active the virtual environment where bomcheck and bomcheckgui \n'
                     '   are stored (i.e., at ' + str(venvpathname) + ').'],
           'bc': ['py -m pip install --upgrade bomcheck',
                  'Upgrade bomcheck to the latest version.'],
           'bcgui': ['py -m pip install --upgrade bomcheckgui',
                     'Upgrade bomcheckgui to the latest version.']}

    latest_getbc = latest('getbc')
    local_getbc = local('getbc')
    latest_bc = latest('bomcheck')
    local_bc = local('bomcheck')
    latest_bcgui = latest('bomcheckgui')
    local_bcgui = local('bomcheckgui')

    print()
    print(('Latest version of ' + fileName + ': ' +
           '.'.join([str(i) for i in latest_getbc]))    if latest_getbc else '')
    print(('Local version of ' + fileName + ': ' +
           '.'.join([str(i) for i in local_getbc]))     if local_getbc else '')
    print(('Latest version of bomcheck: ' +
           '.'.join([str(i) for i in latest_bc]))       if latest_bc else '')
    print(('Local version of bomcheck: ' +
           '.'.join([str(i) for i in local_bc]))        if local_bc else '')
    print(('Latest version of bomcheckgui: ' +
           '.'.join([str(i) for i in latest_bcgui]))    if latest_bcgui else '')
    print(('Local version of bomcheckgui: ' +
           '.'.join([str(i) for i in local_bcgui]))     if local_bcgui else '')

    # Collect commands that need executed, and their help info
    cmdlist = []
    infolist = []

    if (latest_bc > local_bc) or (latest_bcgui > local_bcgui):
        cmdlist.append(dic['activt'][0])
        infolist.append(dic['activt'][1])
    if latest_bc > local_bc:
        cmdlist.append(dic['bc'][0])
        infolist.append(dic['bc'][1])
    if latest_bcgui > local_bcgui:
        cmdlist.append(dic['bcgui'][0])
        infolist.append(dic['bcgui'][1])

    # print info to users explaing what commands are about to be executed.
    if cmdlist:
        print('\nCommands that will be activated:\n')
        i = 0
        for cmd in cmdlist:
            i += 1
            print(str(i) + ') ' + cmd)
        print('')
        i = 0
        for info in infolist:
            i += 1
            print(str(i) + ') ' + info)
    else:
        print("\nbomcheckgui and/or bomcheck is up-to-date. No action will be taken.")
        if latest_getbc > local_getbc:
            print('This program is not designed to update getbc')
        return

    print()
    if flag:
        x = input('Execute commands (takes a couple of minutes). Continue? (Y/N) ')
        if x.lower().strip()[0] == 'y':
            print('working...')
            commands = ' && '.join(cmdlist) + ' && echo commands executed successfully'
            os.system(commands)
        else:
            print('You are not running a MS OS.  No action will be taken.')


def local(package):
    ''' Look on the local computer and find out the version no. of "package".

    Parameters
    ----------
    package: str
        Name of the package located locally.  Only bomcheck, bomcheckgui, and
        the name of this package are valid names for package.

    Returns
    -------
    out : list
       The list is the version, e.g.: [1, 9, 6] for version 1.9.6.  If package
       is not found on pypi.org, return [-1, -1, -1]
    '''

    if package == 'bomcheck':
        package = Path.joinpath(venvpathname, 'lib', 'site-packages', 'bomcheck.py')
    elif package == 'bomcheckgui':
        package = Path.joinpath(venvpathname, 'lib', 'site-packages', 'bomcheckgui.py')
    elif package == fileName:
        return [int(i) for i in __version__.split('.')]
    else:
        print('Bad argument given to function "local"')

    if Path.exists(package):
        with open(package, 'r') as fp:
            lines = fp.readlines()
            for line in lines:
                line = line.strip()
                if '__version__' in line:
                    index1 = line.find("'") + 1
                    index2 = line.find("'", index1 + 1)
                    local_version = line[index1:index2]
                    return  [int(i) for i in local_version.split('.')]
    else:
        return []


def latest(package):
    ''' Look on the pypi.org website and check if there is a later version of
    "package" available.

    Parameters
    ----------
    package: str
        Name of the package located on pypi.org that you want the version
        number of.

    Returns
    -------
    out : list
       The list is the version, e.g.: [1, 9, 6] for version 1.9.6.  If package
       is not found on pypi.org, return [-1, -1, -1]
    '''
    try:
        response = requests.get(f'https://pypi.org/pypi/{package}/json', timeout=5)
        latest_version = response.json()['info']['version']
        return [int(i) for i in latest_version.split('.')]
    except KeyError:
        return []
    except requests.ConnectionError:
        print('No Internet connection available')
        return []


def findDesktop():
    ''' Find the path to the users Desktop directory.  Start from the users
    home directory. Look a couple of levels deep.

    Returns
    -------
    string
        Path to users Desktop directory, e.g 'C:/john/Desktop'.  If not found,
        return users home directory.
    '''
    global desktopnotfound
    desktopnotfound = False
    desktop1 = glob.glob(str(Path.joinpath(Path.home(), 'Desktop'))) # one level deep
    desktop2 = glob.glob(str(Path.joinpath(Path.home(), '*', 'Desktop'))) # two levels deep
    if desktop1:
        return desktop1[0]
    elif desktop2:
        return desktop2[0]
    else:
        desktopnotfound = True
        return str(Path.home())









try:
    app = QApplication(sys.argv)
    cb=app.clipboard()
except:
    pass


venvname = 'bc-venv'
venvpathname = Path.joinpath(Path.home(), venvname)
activate = Path.joinpath(Path.home(), venvname, 'Scripts', 'activate.bat')
linkto = os.path.join(findDesktop(), 'bomcheckgui.exe')
linkfrom = Path.joinpath(Path.home(), venvname, 'Scripts', 'bomcheckgui.exe')
flag = True


if __name__=='__main__':
    main()




