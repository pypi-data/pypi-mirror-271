from templated_setup import Setup_Helper

DESC = """
recursively searches for files based on their extensions starting from a specified directory. It can print the directory structure, include or exclude specific files, use syntax highlighting for output, and anonymize file paths for privacy.
"""

Setup_Helper.init(".templated_setup.cache.json")
Setup_Helper.setup(
	name= "routput",
	author="matrikater (Joel Watson)",
	description=DESC.strip(),
)
