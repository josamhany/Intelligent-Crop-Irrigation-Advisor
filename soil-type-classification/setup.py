#setup.py is use to convert your project into packages it Turns your Python project into a reusable package, and Lets others install your project using pip install . or pip install git+URL.

from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]:
    # this function will return the list of requirements
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements

setup(
    name='Soil-Type-Classification-System',
    version='0.0.1',
    author='RiyankVaghasiya',
    author_email='vaghasiyariyank@gmail.com',
    packages=find_packages(),
    install_requires = get_requirements('requirements.txt')
    
)