from distutils.core import setup

setup(
    name='pyudc',
    packages=['pyudc'],
    version='0.1',
    license='MIT',
    description='Python Universal database connector',
    author='THE UMANG CHAUDHARY',
    author_email='umang3934@gmail.com',
    url='https://github.com/umangrchaudhary/pyudc',
    download_url='https://github.com/umangrchaudhary/pyudc/archive/refs/tags/v1.tar.gz',
    keywords=['python', 'all db', 'database', 'universal database', 'python universal database connection',
              'database connectoin', 'python all database connection'],
    install_requires=[
        'cx-Oracle',
        'dnspython',
        'mysql-connector-python',
        'pkg_resources',
        'psycopg2',
        'psycopg2-binary',
        'pymongo',
        'pyodbc'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)
