import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="torchoptics",
    version="0.0.0a1",
    author="Matthew Filipovich",
    author_email="matthew.filipovich@physics.ox.ac.uk",
    description="Differentiable diffractive optics simulator using PyTorch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url=,
    # project_urls={
    #     "Documentation":,
    #     "Bug Tracker":,
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    license="MIT License",
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.7",
    # install_requires=["torch"],
)
