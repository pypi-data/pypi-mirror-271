import setuptools 


setuptools.setup(
    name='tellon',
    version='0.4',
    author='Ali-Mahmoud-Fadhil',
    description='Hi ! By This Lib You Can Use Tellonym Tools And APIs ,',
    packages=setuptools.find_packages(),
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=['requests','cloudscraper']
)