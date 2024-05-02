from setuptools import setup, find_packages
import pytoolbase
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='pytoolbase',
    version=pytoolbase.__version__,
    packages=find_packages(exclude=['tests']),
    url='https://github.com/mminichino/pytoolbase',
    license='MIT License',
    author='Michael Minichino',
    python_requires='>=3.8',
    install_requires=[],
    author_email='info@unix.us.com',
    description='Python Utility Collection',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=["utilities", "decorator", "retry", "synchronize"],
    classifiers=[
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: MIT License",
          "Intended Audience :: Developers",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Topic :: Software Development :: Libraries",
          "Topic :: Software Development :: Libraries :: Python Modules"],
)
