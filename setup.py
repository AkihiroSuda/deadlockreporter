from distutils.core import setup
setup(
    name='deadlockreporter',
    packages=['deadlockreporter'],
    version='0.0.1',
    description='dumps the stack on deadlock',
    author='Akihiro Suda',
    author_email='suda.akihiro@lab.ntt.co.jp',
    url='https://github.com/AkihiroSuda/deadlockreporter',
    download_url='https://github.com/AkihiroSuda/deadlockreporter/tarball/v0.0.1',
    license='Apache License 2.0',
    scripts=['bin/deadlockreporter'],
    install_requires=[
        'psutil',
    ],
    keywords=['deadlock', 'debug', 'java'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Java',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
