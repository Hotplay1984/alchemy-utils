from setuptools import setup, find_packages

setup(
	name="alchemy-utils",
	version="0.1.0",
	description="Common utilities for alchemy projects",
	author="Your Name",
	packages=find_packages(),
	install_requires=[
		"typing;python_version<'3.5'",  # 根据需要添加依赖
	],
	python_requires=">=3.6"
) 