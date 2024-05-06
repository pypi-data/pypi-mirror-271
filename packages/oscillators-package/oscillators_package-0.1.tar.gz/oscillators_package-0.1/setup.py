from setuptools import setup, find_packages

setup(
    name="oscillators_package",
    version="0.1",
    author="Pradeep Kumar Rebbavarapu",
    author_email="rpkiit2022@gmail.com",
    description="A package for simulating oscillators",
    long_description='kuramoto oscillator package',
    long_description_content_type="text/markdown",
    url="https://github.com/Pradeep-Kumar-Rebbavarapu/CS-208-PROJECT-ODE-GRAPHER/module/oscillators.py",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "numba",
        "matplotlib",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)