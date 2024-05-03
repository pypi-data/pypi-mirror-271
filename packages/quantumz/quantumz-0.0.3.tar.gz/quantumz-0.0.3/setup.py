import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(name="quantumz",
	version="0.0.3",
	author="Sergei Zuev",
	author_email="shoukhov@mail.ru",
	description="A module for quantum computing emulations",
	packages=setuptools.find_packages(),
	long_description=long_description,
	long_description_content_type="text/markdown",
	classifiers=[
		"Programming Language :: Python :: 3.10",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)

