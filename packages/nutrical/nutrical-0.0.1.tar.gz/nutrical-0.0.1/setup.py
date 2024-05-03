import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nutrical", # Replace with your own username
    version="0.0.1",
    author="Yongfu Liao",
    author_email="liao961120@gmail.com",
    description="Nutrition calculation for recipes and ingredients",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liao961120/nutrical",
    # package_dir = {'': 'src'},
    packages=['foodie'],
    install_requires=[
        'Pint',
    ],
    package_data={
        "": ["../data/TW_FDA_nutrition_items.csv"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
