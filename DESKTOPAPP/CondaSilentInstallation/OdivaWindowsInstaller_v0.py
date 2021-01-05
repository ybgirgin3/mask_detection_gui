# download file from powershell# Change this...

import os

# this functions downloads miniconda3 exe file using powershell
# no root-prev required
def ps_installer():
    # download file
    import subprocess

    url = 'https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe'
    output = 'miniconda3-latest-x86_64.exe'
    command = f"Invoke-WebRequest -Uri {url} -OutFile {output}"
    process = subprocess.Popen(["powershell", command])


# this function run miniconda3.exe as admin and silent to install it 
def cmd_admin_silent_runner():
    import ctypes, sys

    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAdmin()
        except: 
            return False

    if is_admin():
        # run and terminate the command prompt
        # this command install miniconda3 on windows using pre-installed exe file
        os.system('cmd /c "miniconda3-latest-x86_64.exe /InstallationType=AllUsers /RegisterPython=1 /S"')


# install required packages in anaconda python
def install_req_packages():
    ## locate default python in anaconda promt
    #username = os.getlogin()
    userprof = os.environ['USERPROFILE']


    ## cmd üzerinden kullandığımız komutlar admin olarak yükleme yapıyor
    # aşağıdaki komutlar bu sebepten değişebilir
    miniconda_base = f'{userprof}\\AppData\\Local\\Continuum\\miniconda3\\conda.exe'
    miniconda_python = f'{userprof}\\AppData\Local\\Continuum\\miniconda3\\python.exe'





