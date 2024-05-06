import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pincode_generator_or_validator',                    
    version="0.0.1",                       
    author="Soumya Roy",                    
    author_email="roysoumya321@gmail.com",
    description="Pin Generator Package to generate Indian valid pin codes and also it can validate the Indian pin codes",
    long_description=long_description,      
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),   
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                     
    python_requires='>=3.6',               
    py_modules=["pincode_generator_or_validator"],             
    install_requires=[]                     
)