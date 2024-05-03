from setuptools import setup 
  
setup( 
    name='ProjectEngine', 
    version='0.2.1', 
    description='Basic PyOpenGl project', 
    author='Oliver Wilkinson', 
    author_email='otwilkinsonuk@icloud.com', 
    packages=['ProjectEngine'], 
    install_requires=[ 
        'pygame', 
        'PyOpenGl',
    ], 
) 
