from setuptools import setup, find_packages
from AIReviewer import __version__

setup(
    name='AIReviewer',
    version=__version__,
    author='Petr Pejsa',
    author_email='petr.pejsa@mbeng.cz',
    description='Short description',

    packages=find_packages(),
    package_data={'': ['res/*.exe']},

    install_requires=['openai', 'pylint', 'streamlit', 'streamlit-ace'],
    extras_require={'test': ['pytest-runner', 'pytest', 'TestConfiguration', 'pytest-cov']},
    zip_safe=True,
    test_suite="tests",
)
