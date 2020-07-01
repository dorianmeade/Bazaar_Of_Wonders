from setuptools import setup

setup(
    name='bazaar_of_wonders',
    version='0.0.0.1',
    packages=['bazaar_of_wonders','main','bazaar_of_wonders_server_scripts','bazaar_of_wonders_db'],
    description='Sample Django pip Project',
    install_requires=['django-tinymce4-lite','django-materializecss-form','PyYAML'],

    entry_points =
    { 'console_scripts':
        [
            'runmyserver = bazaar_of_wonders_server_scripts.run:main',
#            'initmyserver = bazaar_of_wonders_server_scripts.init:main',
        ]
    },
    include_package_data=True
)
