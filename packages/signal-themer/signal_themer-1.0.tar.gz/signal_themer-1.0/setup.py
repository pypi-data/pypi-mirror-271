from pathlib import Path
from setuptools import setup

setup_dir = Path(__file__).resolve().parent

setup(
    include_package_data=True,
    name='signal-themer',
    version='1.0',
    author='Kritagya Bhattarai(CalfMoon)',
    author_email='kritagyabhattarai@proton.me',
    packages=['signal_themer'],
    install_requires=['asarPy'],
    entry_points={
        'console_scripts': ['signal-themer = signal_themer.__main__:theme_injector']
    },
    url='https://github.com/CalfMoon/signal-themer',
    description='Theme injector for signal-desktop',
    long_description=Path(setup_dir, 'README.md').open().read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
    ]
)
