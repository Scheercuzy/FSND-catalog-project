from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='Item Catalog Application Project',
    version='0.1a',
    python_requires='>=3.5',
    description="""An application that provides a list of items within
    a variety of categories as well as provide a user registration and
    authentication system. Registered users will have the ability to
    post, edit and delete their own items.""",
    long_description=readme(),
    # url='',
    author='MX',
    author_email='maxi730@gmail.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[requirements]
)
