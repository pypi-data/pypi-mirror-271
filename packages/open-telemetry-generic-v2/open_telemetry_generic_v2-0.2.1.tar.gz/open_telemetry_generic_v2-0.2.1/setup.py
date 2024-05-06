from setuptools import setup, find_packages

setup(
    name='open_telemetry_generic_v2',
    version='0.2.1',
    description='A generic function to be able to use for open telemtry cases',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Atif Agboatwala',
    author_email='atif.agboat@hotmail.com',
    url='https://github.com/yourusername/my_package',
    # package_dir={'': 'otel-getting-started'},
    # packages=find_packages(where='otel-getting-started'),
    install_requires=[
        # List your project's dependencies here.
        # They will be installed by pip when your project is installed.
        "opentelemetry",
        "functools",
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.11',
    ],
)
