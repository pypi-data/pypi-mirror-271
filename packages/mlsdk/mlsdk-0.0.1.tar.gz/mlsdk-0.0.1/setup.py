from setuptools import setup, find_packages

setup(
    name='mlsdk',
    version='0.0.1',
    packages=find_packages(),
    description='Model Zoo SDK',
    long_description=open('README.md').read(),
    install_requires=[
        'boto3',
        'python-dotenv',
        'silabs-mltk[full]'
    ],
    author='EUR',
    author_email='eur@gmail.com',
    license='MIT',
    entry_points={
        "console_scripts": [
            "mlsdk = mlsdk.__main__:main"
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
