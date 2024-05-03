from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='yaml-to-docker',
    version='0.1',
    license='MIT',
    description='Script to Convert YAML to Docker',
    long_description=readme(),
    author='Alexander Krefting',
    author_email='linuxdevalex@outlook.de',
    url='https://github.com/androlinuxs/termux-music',
    scripts=['yaml-to-docker'],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3'
    ]
)
