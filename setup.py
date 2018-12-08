import setuptools


setuptools.setup(
    name='maelstrom',
    version='0.0.1',
    author='Andrew Rabert',
    author_email='arabert@nullsum.net',
    url='https://github.com/nvllsvm/maelstrom',
    license='GPLv3',
    packages=['maelstrom'],
    package_data={
        'maelstrom': ['templates/*'],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only'
    ],
    python_requires='>=3.6',
    install_requires=['tornado>=5'],
    entry_points={'console_scripts': ['maelstrom=maelstrom.app:run']}
)
