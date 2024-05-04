import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
  
setuptools.setup( 
    name="random-file-generator", 
    version="0.0.2",
    author="NishithRaveeshKashyap", 
    author_email="nishithkp175@gmail.com", 
    packages=["random-file-generator"],
    description='Generate random text files',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NishithKashyap/Generate-Random-Files", 
    license='MIT', 
    python_requires='>=3.8',
    install_requires=[],
)
