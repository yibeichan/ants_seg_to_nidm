#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages
from os.path import join as opj
from os.path import dirname


def get_version():
    """Load version only
    """
    with open(opj(dirname(__file__), 'ants_seg_to_nidm', '__init__.py')) as f:
        version_lines = list(filter(lambda x: x.startswith('__version__'), f))
    assert (len(version_lines) == 1)
    return version_lines[0].split('=')[1].strip(" '\"\t\n")

# extension version
version = get_version()
PACKAGES = find_packages()

README = opj(dirname(__file__), 'README.md')
try:
    import pypandoc
    long_description = pypandoc.convert(README, 'rst')
except (ImportError, OSError) as exc:
    print(
        "WARNING: pypandoc failed to import or threw an error while converting"
        " README.md to RST: %r  .md version will be used as is" %exc
    )
    long_description = open(README).read()

# Metadata
setup(
    name='ants_seg_to_nidm',
    version=version,
    description='ANTS segmentation data to NIDM / jsonld',
    long_description=long_description,
    author='David Keator',
    author_email='dbkeator@uci.edu',
    url='https://github.com/dbkeator/ants_seg_to_nidm',
    packages=PACKAGES,
    install_requires=[
        'numpy',
        # Kept in lockstep with the consuming BIDSapp's top-level
        # requirements.txt. The old 'pynidm==4.2.4' here made pip warn
        # ("ants-seg-to-nidm 0.0.1 requires pynidm==4.2.4, but you have pynidm
        # 4.5.0") on every container build and would have pulled 4.2.4 back in
        # for anyone installing this package on its own.
        'pynidm==4.5.0',
        'pandas',
        # prov 3.0.0 moved NetworkX graph interop to an optional extra that
        # nidm.experiment imports; without it importing this package fails.
        'prov[graph]',
        # Deliberately loose, and it must stay that way: pynidm 4.5.0 declares
        # rdflib~=6.3.2, so pinning rdflib>=7 *here* makes this package's own
        # metadata self-contradictory and `pip install -e .` dies with
        # ResolutionImpossible. The runtime actually wants rdflib 7.x (oxrdflib
        # needs <8), and the consuming container gets there with an explicit
        # `pip install --upgrade 'rdflib>=7.0.0,<8'` step *after* this install --
        # a deliberate override, which pip reports as a warning rather than an
        # error. Same arrangement as the sibling freesurfer app's segstats_jsonld.
        'rdflib>=6.0',
    ], # Add requirements as necessary
    include_package_data=True,
    extras_require={
        'devel-docs': [
            # for converting README.md -> .rst for long description
            'pypandoc',
        ]},
    entry_points={
        'console_scripts': [
            'antsegstats2nidm=ants_seg_to_nidm.ants_seg_to_nidm:main' # this is where the console entry points are defined
            ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], # Change if necessary
)
