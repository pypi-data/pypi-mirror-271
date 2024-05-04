import setuptools 


setuptools.setup(
    name='xvlib',
    version='0.2',
    author='Aymen M.',
    description='This lib will be updated every some months , helps you check username telegram status , auction taken available , and colorize your terminal and save file data and new some GPT talking , making Images .',
    packages=setuptools.find_packages(),
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=['requests','bs4']
)