import setuptools


setuptools.setup(
    name='maelstrom',
    author='Andrew Rabert',
    author_email='ar@nullsum.net',
    url='https://github.com/nvllsvm/maelstrom',
    license='GPLv3',
    packages=['maelstrom'],
    package_data={
        'maelstrom': ['static/*', 'templates/*'],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only'
    ],
    python_requires='>=3.6',
    install_requires=['tornado>=5'],
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    entry_points={'console_scripts': ['maelstrom=maelstrom.app:run']}
)
