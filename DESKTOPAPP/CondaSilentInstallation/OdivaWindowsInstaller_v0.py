# download file from powershell# Change this...

import os
# no root-prev required


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


    # herhangi bir conda env oluşturma işlemi olmayacağından dolayı 
    # pip kullanmak yerine "python3 -m pip" kullanmak daha mantıklı olabilir


    ## /home/berkay/miniconda3/envs/all_/bin/python3 -m pip
    # linuxte komutunu kullnarak base içindeyken all_ içindeki pip modülüne ulaşabiliyorum
    # miniconda_python komutunu kullanarak gerekli python yüklemelerini yapabilirim

    














