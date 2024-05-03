from templated_setup import templated_setup

DESCRIPTION = "A quick and easy replacement for some `setup.py` implementations."

templated_setup.Setup_Helper.init(".templated_setup_cache.json")
templated_setup.Setup_Helper.setup(
	name="templated-setup",
	author="matrikater (Joel Watson)",
	description=DESCRIPTION,
	author_email="administraitor@matriko.xyz",
	install_requires=[
		"setuptools",
		"twine"
	],
)
