from setuptools import setup, find_packages

setup(
    name='communication_services',
    version='0.1.2',
    author='genius studio',
    author_email='info@geniusai.com',
    description='A short description of your project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/geniusai1/partialtruckload-communication-serivecs.git',  # Link to your project's GitHub repo
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Add your project dependencies here
        # 'requests',
        # 'numpy',
        'celery',
        'twilio',
        'firebase-admin',

    ],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)
