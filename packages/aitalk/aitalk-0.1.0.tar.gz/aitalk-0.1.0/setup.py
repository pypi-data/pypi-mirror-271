from setuptools import setup, find_packages

setup(
    name='aitalk',
    version='0.1.0',
    author='Imane Mtq',
    author_email='imottaqi@archipel.group',
    description='A speech assistant package',
    packages=find_packages(),
    install_requires=open('requirements.txt').readlines(),
    include_package_data=True,  # This tells setuptools to check MANIFEST.in for non-code files
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        "Operating System :: Microsoft :: Windows",
    ],
    
)
