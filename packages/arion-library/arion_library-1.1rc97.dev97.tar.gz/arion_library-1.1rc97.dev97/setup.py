
from setuptools import setup, find_packages

setup(
    name='arion_library',
    version='1.1rc97.dev97',  
    author='Heni Nechi',  
    author_email='h.nechi@arion-tech.com',  
    url='https://github.com/Ariontech/ArionLibrary.git',  
    packages=find_packages(),  
    python_requires='>=3.8',  
    install_requires=['pyodbc', 'pytest', 'pysftp==0.2.9', 'ShopifyAPI==12.5.0', 'requests==2.31.0', 'azure-core==1.29.6', 'azure-data-tables==12.5.0', 'azure-storage-blob==12.19.1', 'python-dotenv==1.0.1', 'pytest==8.1.1', 'pandas==2.0.3', 'pytest'],
)