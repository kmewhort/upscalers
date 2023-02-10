import setuptools

setuptools.setup(
    name="upscalers",
    version="0.5.2",
    description="AI upscaling of images",
    author="Kent Mewhort",
    author_email="kent@openissues.ca",
    url='https://github.com/kmewhort/upscalers',
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    include_package_data=True,
    python_requires='>=3.7',
)
