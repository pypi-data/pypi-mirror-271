from setuptools import setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\\n" + fh.read()

setup(
    name="parseid",
    version='0.2.0',
    author="Tiezheng Yuan",
    author_email="tiezhengyuan@hotmail.com",
    description="suck, parse identifiers or accession numbers",
    url = "https://github.com/Tiezhengyuan/parse_identifier",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=['parseid'],
    package_dir={'': 'src'},
    install_requires=[
        'bioomics',
        'numpy',
        'pandas',
        'requests',
        'obonet',
        'python-dotenv'
    ],
    keywords=['pypi', 'cicd', 'python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)
