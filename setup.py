"""
OpenFF NAGL Models
Models used with NAGL
"""
import sys
from setuptools import setup, find_namespace_packages
import versioneer

short_description = "Models used with NAGL.".strip().split("\n")[0]

# from https://github.com/pytest-dev/pytest-runner#conditional-requirement
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

try:
    with open("README.md", "r") as handle:
        long_description = handle.read()
except:
    long_description = "\n".join(short_description[2:])


setup(
    name='openff-nagl-models',
    author='Lily Wang',
    author_email='lily.wang@openforcefield.org',
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license='MIT',
    packages=find_namespace_packages(include=['openff.*']),
    include_package_data=True,
    python_requires=">=3.9",          # Python version restrictions
    setup_requires=[] + pytest_runner,
    install_requires=["importlib_resources"],
    platforms=['Linux',
               'Mac OS-X',
               'Unix'],
    extras_require={
        "test": [
            "pytest>=6.0",
            "numpy"
        ],
    },

    entry_points={
        "openforcefield.nagl_model_directory": [
            "get_nagl_model_dirs_paths = openff.nagl_models:get_nagl_model_dirs_paths",
        ]
    }
)
