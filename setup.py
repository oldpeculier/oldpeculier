import os
import sys
from setuptools import setup, find_packages
CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Operating System :: POSIX :: Linux',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Software Development :: Libraries',
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7"
]
requires = []
tests_require = []
here = os.path.abspath(os.path.dirname(__file__))
testsuite="oldpeculier.tests.unit"
#if "--all" in sys.argv:
#    testsuite="oldpeculier.tests"
#    sys.argv.remove("--all")
#elif "--live" in sys.argv:
#    testsuite="oldpeculier.tests.live"
#    sys.argv.remove("--live")
#elif "--unit" in sys.argv:
#    sys.argv.remove("--unit")

try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except:
    README = ''
    CHANGES = ''
dist = setup(
    name='oldpeculier',
    version='0.0.1',
    license='Apache (http://www.apache.org/licenses/LICENSE-2.0)',
    url='http://github.com/oldpeculier/oldpeculier',
    description="Software to aid in the creation and deployment of system architectures",
    long_description=README + '\n\n' + CHANGES,
    classifiers=CLASSIFIERS,
    author="Chava Jurado",
    author_email="chava.jurado@gmail.com",
    maintainer="Chava Jurado",
    maintainer_email="chava.jurado@gmail.com",
    packages=find_packages(),
    install_requires=requires,
    tests_require=tests_require,
    include_package_data=True,
#    zip_safe=False,
    test_suite=testsuite,
)
