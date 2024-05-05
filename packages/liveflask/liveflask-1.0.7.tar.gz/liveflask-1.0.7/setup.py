from setuptools import setup, find_packages

with open("readme_pypi.md", "r") as fh:
    long_description = fh.read()

setup(
    name="liveflask",
    version="1.0.7",
    author="Jarriq Rolle",
    author_email="jrolle@baysidetechgroup.com",
    description="Seamlessly integrate modern reactive components into Flask templates, eliminating the need for mastering new templating languages or wrestling with complex JavaScript frameworks. With our solution, developers can enhance their Flask applications with dynamic functionality while maintaining a familiar development environment, streamlining the process and ensuring a smoother user experience.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JarriqTheTechie/liveflask",
    packages=['liveflask'],
    package_data={'liveflask': ['**/*']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        "flask",
        "masonite-orm",
        "Flask-WTF"
    ],
)
