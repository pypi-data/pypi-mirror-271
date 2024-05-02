from setuptools import setup, find_packages
#packages=find_packages()
#packages=['robin_api'],
setup(
    name='robin_api',
    version='1.2',
    packages=find_packages(),
    description="file",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'httpx',
        'pydantic',
        'distro'
    ],
    python_requires='>=3.9',
    author='William Gomez',
    author_email='william.gomez712@gmail.com',
    url='https://github.com/williamgomez71/RobinApi',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)