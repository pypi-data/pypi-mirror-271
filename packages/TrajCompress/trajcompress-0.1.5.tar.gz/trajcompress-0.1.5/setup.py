from setuptools import setup, find_packages

setup(
    name="TrajCompress",
    version="0.1.5",
    # packages=find_packages('TrajCompress'),
    packages=find_packages(),
    install_requires=[
        # 'argparse',  
        # 'os',
        # 'math',
        'pandas',
        'tqdm',
    ],
    author='jijivski',
    author_email='jijivski@outlook.com',
    url='https://github.com/jijivski/TrajCompress',  # URL to the repository
)


#python -m pip install --upgrade build