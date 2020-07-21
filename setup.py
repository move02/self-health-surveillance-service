from setuptools import setup, find_packages

setup(
    name='My-Flask-CI',
    packages=find_packages(),
    version='0.1',
    long_description=__doc__,
    zip_safe=False,
    test_suite='nose.collector',
    include_package_data=True,
    install_requires=[
        'alembic==1.4.2',
        'click==7.1.2',
        'Flask==1.1.2',
        'Flask-Migrate==2.5.3',
        'Flask-Script==2.0.6',
        'Flask-SQLAlchemy==2.4.4',
        'SQLAlchemy==1.3.18',
        'itsdangerous==1.1.0',
        'Jinja2==2.11.2',
        'MarkupSafe==1.1.1',
        'Werkzeug==1.0.1',
        'python-dateutil==2.8.1',
        'python-dotenv==0.14.0', 
        'python-editor==1.0.4'  
    ],
    tests_require=['nose'],
)