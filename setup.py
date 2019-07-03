from setuptools import setup
import json


with open('metadata.json') as fp:
    metadata = json.load(fp)


setup(
    name='lexibank_bodtkhobwa',
    version="1.0",
    description=metadata['title'],
    license=metadata.get('license', ''),
    url=metadata.get('url', ''),
    py_modules=['lexibank_bodtkhobwa'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'bodtkhobwa=lexibank_bodtkhobwa:Dataset',
        ]
    },
    install_requires=[
        'pylexibank==1.1.1',
        'segments==2.0.2'
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
