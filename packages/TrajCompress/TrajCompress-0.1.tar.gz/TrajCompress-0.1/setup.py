from setuptools import setup, find_packages

setup(
    name="TrajCompress",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # 'argparse',  
        # 'os',
        # 'math',
        'pandas',
        'tqdm',
    ],
    author='jijivski',
    author_email='chenghao.zhu.cn@gmail.com',
    url='https://github.com/jijivski/TrajCompress',  # URL to the repository
)
