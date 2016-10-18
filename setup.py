import sys
from setuptools import setup, find_packages


if sys.version_info[:2] < (3, 5):
    sys.exit('Cage requires Python 3.5 or higher.')

try:
    import pypandoc
    long_description = pypandoc.convert("README.md", "rst")
except (IOError, ImportError):
    long_description = "Develop and run your Python applications in clean Docker environments"

setup_params = {
    "entry_points": {
        "console_scripts": ["cage=cage:main"],
    },
    "zip_safe": False,
}

setup(
    name="PYCage",
    version="0.1.1",
    description="Develop and run your Python applications in clean Docker environments",
    long_description=long_description,
    url="https://github.com/macostea/cage",
    author="Mihai Costea",
    author_email="mihai.andrei.costea@icloud.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
    ],
    keywords="setuptools deployment installation distutils docker",
    py_modules=['cage'],
    packages=find_packages(exclude=["tests", "test_app"]),
    install_requires=["docker-py"],
    include_package_data=True,
    **setup_params
)
