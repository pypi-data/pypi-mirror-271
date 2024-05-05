from setuptools import setup, find_packages
setup(
name='SimpleTKMessageBox',
version='0.2.9',
author='Gustoon',
author_email='no.email@gmail.com',
description='A simple tkinter message box',
long_description="""
See documentation at https://github.com/Gustoon/SimpleTkMessageBox
""",
packages=find_packages(),
install_requires=['Pillow'],
include_package_data=True,
data_files=[
    ('SimpleTkMessageBox/icons', ['SimpleTkMessageBox/icons/transparent.ico']),
    ('SimpleTkMessageBox/icons/W11', ['SimpleTkMessageBox/icons/W11/1.png', 'SimpleTkMessageBox/icons/W11/2.png', 'SimpleTkMessageBox/icons/W11/3.png', 'SimpleTkMessageBox/icons/W11/4.png', 'SimpleTkMessageBox/icons/W11/5.png']),
    ('SimpleTkMessageBox/icons/W10', ['SimpleTkMessageBox/icons/W10/1.png', 'SimpleTkMessageBox/icons/W10/2.png', 'SimpleTkMessageBox/icons/W10/3.png', 'SimpleTkMessageBox/icons/W10/4.png', 'SimpleTkMessageBox/icons/W10/5.png']),
    ('SimpleTkMessageBox/icons/W7', ['SimpleTkMessageBox/icons/W7/1.png', 'SimpleTkMessageBox/icons/W7/2.png', 'SimpleTkMessageBox/icons/W7/3.png', 'SimpleTkMessageBox/icons/W7/4.png', 'SimpleTkMessageBox/icons/W7/5.png']),
],
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)