from setuptools import setup

setup(
    name='dynamic_drf',
    version='0.1',
    description="A package that overrides the default drf spectacular", \
    long_description="This python package is for those developers who feels complex to include drf-spectacular in there project. Now simple add this 'dyn_drf' in your installed apps. Then in your project url import urlpatterns from urlpatterns  \
        Simply do urlpatterns+=[ \
            path('your-other-url',your_views), \
        ]" ,
    author='Atit Sharma',
    packages=['dynamic_drf'],
    install_requires=[
        "Django==5.0.4",
        "drf-spectacular==0.27.2",
        "djangorestframework==3.15.1"
    ]
    

)