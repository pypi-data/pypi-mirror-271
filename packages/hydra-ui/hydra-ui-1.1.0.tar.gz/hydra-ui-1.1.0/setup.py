from setuptools import setup

setup(
	name="hydra-ui",
	version="1.1.0",
	description="A framework for developing hybrid CLI/GUI programs.",
	long_description="Hydra is a framework for developing hybrid CLI/GUI programs in Python. It is a lightweight wrapper around Tk and is pure Python, with no external dependencies.",
	long_description_content_type="text/x-rst",
	url="https://github.com/rweathers/hydra",
	author="Ryan Weathers",
	author_email="ryanweathers63@gmail.com",
	license="GPLv3+",
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"Topic :: Software Development :: Libraries :: Application Frameworks",
		"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
		"Programming Language :: Python :: 3 :: Only"
	],
	py_modules=["hydra"]
)
