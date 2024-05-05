from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'sdk for duwi third platform'

setup(
    name="duwi_smart_sdk",
    version=VERSION,
    author="ledger",
    author_email="ledgerbiggg@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md', encoding="UTF8").read(),
    packages=find_packages(),
    install_requires=['websockets', 'aiohttp'],
    keywords=['python', 'duwi'],
    entry_points={
        'console_scripts': [
            'duwi = duwi_smart_sdk.main:main'
        ]
    },
    license="MIT",
    url="https://github.com/Ledgerbiggg/duwi_smart_sdk",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ]
)
