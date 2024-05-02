from setuptools import setup 
  
setup( 
    name='ProjectEngine', 
    version='0.1', 
    description='Basic PyOpenGl project', 
    author='Oliver Wilkinson', 
    author_email='otwilkinsonuk@icloud.com', 
    packages=['Project-Engine'], 
    install_requires=[ 
        'pygame', 
        'PyOpenGl',
    ], 
) 
