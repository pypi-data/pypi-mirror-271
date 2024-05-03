from templated_setup import templated_setup

DESC = """
recursively searches for files based on their extensions starting from a specified directory. It can print the directory structure, include or exclude specific files, use syntax highlighting for output, and anonymize file paths for privacy.
"""

templated_setup.Setup_Helper.init(".templated_setup.cache.json")
templated_setup.Setup_Helper.setup(
	name= "routput",
	author="matrikater (Joel Watson)",
	description=DESC.strip(),
)
