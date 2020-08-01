from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='django-bazaar-of-wonders',
    author='https://github.com/Bazaar-Trader',
    version='0.1.40',
    
    description='Bazaar of Wonders is a Django-based web application that aggregates card details and pricing statistics for trading card games, namely, Magic: The Gathering.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    url="https://github.com/Bazaar-Trader/Bazaar_Of_Wonders",
    packages=['bazaar_of_wonders','main','bazaar_of_wonders_server_scripts','bazaar_of_wonders_db'],
    include_package_data=True,
    install_requires=['django','django-tinymce4-lite','django-materializecss-form','PyYAML','bs4','django-environ','apscheduler'],
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    
    entry_points =
    { 'console_scripts':
        [
            'bazaar_start = bazaar_of_wonders_server_scripts.run:main',
        ]
    },
    
)
