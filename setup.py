from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()



setup(
    name='gdpr-consent-string',
    description='Python implementation of parser for GDPR consent string',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/AccesoGroup/gdpr-consent-string',
    version='0.1',
    python_requires='>=3.5',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5'
    ],
    packages=['GDPRconsent']
)