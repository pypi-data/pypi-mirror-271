from setuptools import setup, find_packages
import codecs
import os
here = os.path.abspath(os.path.dirname(__file__))
print(find_packages())
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.3'
DESCRIPTION = 'Display syntax highlighted code in customtkinter'
LONG_DESCRIPTION = 'This is a package for displaying code with syntax highlighting in a customtkinter application.'

# Setting up
setup(
    name="CustomtkinterCodeViewer",
    version=VERSION,
    author="Rigved Maanas",
    author_email="<rigvedmaanas@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["customtkinter", "packaging", "pygments"],
    keywords=['python', 'customtkinter', 'code view', 'code viewer', 'CTkCodeViewer', 'tkinter'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)