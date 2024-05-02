from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(
    name='DE_DataBaseConnect',
    version='0.0.83',
    license="MIT",
    author='Almir J Gomes',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='almir.jg@hotmail.com',
    keywords="Database connect",
    description='Conector com varias base de dados',
    #packages=find_packages(),
    url='https://github.com/DE-DataEng/DE_DataBaseConnect.git',
    #install_requires=["sqlalchemy", "cx_Oracle", "sqlite3", "psycopg2", "mysql.connector", "pymssql", "redshift_connector", "fdb", "jaydebeapi", "jpype"]
)
