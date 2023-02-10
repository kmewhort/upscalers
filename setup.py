import setuptools

setuptools.setup(
    name="upscalers",
    version="0.5.3",
    description="AI upscaling of images",
    long_description="Upscalers provides an easy way to apply image upscaling using a variety of AI upscalers (including ESRGAN, R-ESRGAN, ScuNET, and SwinIR)",
    author="Kent Mewhort",
    author_email="kent@openissues.ca",
    url='https://github.com/kmewhort/upscalers',
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    include_package_data=True,
    python_requires='>=3.7',
)
