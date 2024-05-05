from setuptools import setup, find_packages

with open("README.md","r") as f:
    description = f.read()


VERSION = '0.0.1'
S_DESCRIPTION = 'EPIAS Transparency Platform 2.0 Unofficial Python Library'

# Setting up
setup(
    name="seffaflik2",
    version=VERSION,
    author="Berk Ömer Atay",
    author_email="<berkomeratay@gmail.com>",
    description=S_DESCRIPTION,
    long_description = description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/berkomeratay/seffaflik2",
    packages=find_packages(),
    install_requires=['requests', 'pandas', 'numpy'],
    keywords=['python', 'epias', 'seffaflik', 'epias transparency platform', 'transparency', 'epiaş şeffaflık platformu'],
    
)