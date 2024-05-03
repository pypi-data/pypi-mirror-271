from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pytom3d",
    version="0.0.0rc3",
    description="PyToM-3D: Python Topography Manipulator in 3D",
    long_description=long_description,
    long_description_content_type="text/markdown",
        
    author="Alessandro Tognan",
    author_email="alessandro.tognan@gmail.com",
    url="https://github.com/aletgn/pytom-3d.git",
    project_urls = {"Bug Tracker": "https://github.com/aletgn/pytom-3d/issues"},
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=["numpy", "scipy", "matplotlib", 
                      "pandas", "odfpy", "openpyxl",
                      "scikit-learn"],
    extras_require={"test" : ["notebook"],
                    "dev" : ["pytest", "twine", "setuptools", "build"]}
)
