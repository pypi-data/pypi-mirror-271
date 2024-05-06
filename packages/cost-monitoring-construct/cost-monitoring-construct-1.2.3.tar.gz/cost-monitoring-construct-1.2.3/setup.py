import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cost-monitoring-construct",
    "version": "1.2.3",
    "description": "A CDK construct that helps track applications' costs separately and receive alerts in case of unpredicted resource usage",
    "license": "Apache-2.0",
    "url": "https://github.com/DataChefHQ/cost-monitoring-construct.git",
    "long_description_content_type": "text/markdown",
    "author": "DataChef<support@datachef.co>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/DataChefHQ/cost-monitoring-construct.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cost_monitoring_construct",
        "cost_monitoring_construct._jsii"
    ],
    "package_data": {
        "cost_monitoring_construct._jsii": [
            "cost-monitoring-construct@1.2.3.jsii.tgz"
        ],
        "cost_monitoring_construct": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.1.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.80.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
