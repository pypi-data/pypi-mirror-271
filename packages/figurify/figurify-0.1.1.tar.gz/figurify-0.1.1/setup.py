from setuptools import setup, find_packages

def get_version():
    with open("VERSION.txt", 'r') as f:
        version = f.read().strip()
    return version

setup(
    name='figurify',
    version=get_version(),
    author='Julian Hess',
    description='With figurify you can calculate figures, surfaces and physics.',
    long_description=open("documentation.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    project_urls={
        "Source": "https://github.com/julian-hess/Figurify.git"
    },
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers'
    ],
)
