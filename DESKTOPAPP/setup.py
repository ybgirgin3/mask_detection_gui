import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()



setuptools.setup(
        name = 'Odiva: Mask Detector',
        version = '0.0.1',
        author = 'Yusuf Berkay Girgin',
        author_email = 'ybgirgin3@gmail.com',
        description = 'Implementable Indoor Crowd Mask Detection System',
        long_description = long_description,
        package_dir = {'': 'src'},
        packages = setuptools.find_packages(where='src'),
        install_requires=[
            'imutils',
            'opencv-python==4.1.2.30',
            'PyQt5==5.12',
            'numpy==1.19.4'
        ],
        python_requires='3.7*',


)
