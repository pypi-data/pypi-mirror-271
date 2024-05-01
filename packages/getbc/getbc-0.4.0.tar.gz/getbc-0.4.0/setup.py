'''
setup.py for getbc.py.
'''

from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='getbc',   # name people will use to pip install
    python_requires='>=3.8',
    version='0.4.0',
    description='Make installing bomcheckgui easy',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='GPLv3+',
    py_modules=['getbc'],
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',],
    url='https://github.com/kcarlton55/getbc',
    author='Kenneth Edward Carlton',
    author_email='kencarlton55@gmail.com',
    entry_points={'console_scripts': ['getbc=getbc:main']},
    keywords='bomcheckgui',
)
