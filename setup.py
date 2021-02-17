import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="scheduler_api_template_py",
    version="0.0.1",

    description="An empty CDK Python app",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="author",

    package_dir={"": "scheduler_api_template_py"},
    packages=setuptools.find_packages(where="scheduler_api_template_py"),

    install_requires=[
        "aws-cdk.core==1.86.0",
        "aws-cdk.aws_dynamodb==1.86.0",
        "aws-cdk.aws_lambda==1.86.0",
        "aws-cdk.aws_apigateway==1.86.0",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
