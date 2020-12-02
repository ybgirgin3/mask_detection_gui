from setuptools import setup, find_packages


setup(
        name = 'Odiva',
        version = '0.0.0',
        description = 'Easy Implementable Mask Detection System',
        author = 'Yusuf Berkay Girgin',
        author_email = 'ybgirgin3@gmail.com',
        packages = find_packages(include=['source', 'source/yolo-coco', 'source.*']),
        install_requires=[
            'imutils',
            'opencv-python==4.1.2.30',
            'PyQt5==5.12',
            'numpy==1.19.4'
            ]

        python_requires='3.7.9',
            


    )
