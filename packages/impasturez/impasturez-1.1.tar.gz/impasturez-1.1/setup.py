from distutils.core import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()

setup(
    name = 'impasturez',
    packages = ['impasturez'],
    version = '1.1',
    license='MIT',
    description = 'impasturez',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author = 'Ochaaz',
    author_email = 'ochaaz@gmail.com',
    url = 'https://github.com/ochaaz/impasturez',
    download_url = 'https://github.com/ochaaz/impasturez/archive/v_01.tar.gz',
    project_urls={
        'Documentation': 'https://github.com/ochaaz/impasturez',
        'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/ochaaz/impasturez/',
        'Tracker': 'https://github.com/ochaaz/impasturez/issues',
    },
    keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],
    install_requires=[
            'validators',
            'beautifulsoup4',
            'discordautochat',
            'discorudo',
        ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
     dependencies= [
        'discordautochat',
        'discorudo'
    ]
)
