from setuptools import setup, find_packages

setup(
    name="adpipsvcfuncs",
    version="0.1.5",
    packages=find_packages(),    
    author="Oleg D",
    author_email="olegd@gmail.com",
    description="Service functions for the Adaptive Pipeline Workflow project.",
    license="MIT",
    keywords="GenAI, GCP",
    url="https://github.com/odegay/adaptive-pipeline-service-functions",
    install_requires=[
        'google-secret-manager', 'google-cloud-pubsub', 'requests'
    ]
)