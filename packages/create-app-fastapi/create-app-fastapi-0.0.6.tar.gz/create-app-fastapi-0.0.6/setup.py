from setuptools import setup, find_packages

setup( 
	name="create-app-fastapi", 
	version="0.0.6", 
	author="Ravishnu", 
	author_email="ravishnu60@gmail.com", 
	packages=find_packages(), 
    url="https://github.com/ravishnu60/create-app-fastapi.git",
	description="Library for initializing FastAPI projects - create-app-fastapi", 
	long_description="""A package used to create fastAPI project structure with virtual environment and dependencies.
    Once you install this package use below command to create fastapi project,
    
    create-app-fastapi project-name
    
    """, 
	long_description_content_type="text/markdown", 
	python_requires='>=3.9', 
	install_requires=[],
	entry_points ={ 
		'console_scripts': [ 
			'create-app-fastapi=projectfastapi.main:main'
		] 
	},
    keywords=['fastapi', 'fastapi project','project structure','api structure', 'python fastapi project structure']
) 
