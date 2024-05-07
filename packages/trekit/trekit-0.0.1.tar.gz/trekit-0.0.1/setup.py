from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="trekit",
        version="0.0.1",
        description="A package for useful functions",
        long_description=open("README.md", encoding="utf-8").read(),
        long_description_content_type="text/markdown",
        url="https://github.com/trebladev/trekit",
        author="trebladev",
        author_email="flexiblexuan@gmail.com",
        packages=find_packages(),
        include_package_data=True,
        classifiers=[
            "Programming Language :: Python :: 3",
        ],
        install_requires=[
            "numpy",
            "point_cloud_utils"
        ]

    )
    

    
