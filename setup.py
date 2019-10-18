from setuptools import setup, find_packages
setup(
    name="DevHelper",
    version="0.1",
    author="J. Bates",
    author_email="jbates@sociusmarketing.com",
    description="DevHelper is a simple CLI tool to help ease the process of configuring and managing WP Dev Enviorments ",

    packages=find_packages(),

    install_requires=[
        'click',
        'requests',
        'python-slugify',
        'python-dotenv',
        'mysql-connector'
    ],

    entry_points= {
        'console_scripts': [
            'devhelper=devhelper.devhelper:cli'
        ]
    }
)
