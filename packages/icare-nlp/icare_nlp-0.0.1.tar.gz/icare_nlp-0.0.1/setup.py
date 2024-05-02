from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'From CV detection to answer questions'
# 配置
setup(
    name="icare_nlp",
    version=VERSION,
    author_email="23037086r@connect.polyu.hk",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['icare', 'language']
)