import setuptools

long_desc = open("README.md").read()
required = ["numpy>=1.26", "matplotlib>=2.8.4", "scipy>=1.14"]

setuptools.setup(
    name="odestpy",
    version="1.0.0",
    author="Nahomi Bouza",
    author_email="nahomi.bouza@gmail.com",
    description="Estimate the parameters of a system of ordinary differential equations that are linear with respect "
                "to the parameters",
    long_description=long_desc,
    url="https://github.com/NahomiB/ode-estimation",
    install_requires=required,
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
