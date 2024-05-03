from setuptools import setup, find_packages

with open("README.md",
          "r", encoding="utf-8") as file:
    long_description = file.read()

### xcoll not considered for now

setup(
    name='RFKO_Xsuite',
    version='0.1.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A package for wrapping up some funcitonalities from Xsuite',
    long_description=long_description,
    install_requires=['xsuite','xpart','xobjects','xtrack','xcoll','cpymad','matplotlib'
        ,'numpy', 'pandas'],  # add any additional packages you want to include here
    url='https://gitlab.cern.ch/wscarpa/rfko_xsuite.git',  # replace with your package's url
    author='Wesley',
    author_email='wesley.scarpa@cern.ch'
)


