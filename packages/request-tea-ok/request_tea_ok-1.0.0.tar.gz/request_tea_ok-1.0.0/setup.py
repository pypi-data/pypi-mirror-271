from setuptools import setup

setup(
    author='Wahdalo',
    author_email='ahdx.wtf@gmail.com',
    name='request-tea-ok',
    version='1.0.0',
    description='This function is designed to make HTTP requests to the website app.tea.xyz',
    url='https://github.com/wahdalo/tea-python',
    project_urls={
        'Homepage': 'https://github.com/wahdalo/tea-python',
        'Source': 'https://github.com/wahdalo/tea-python',
    },
    py_modules=['request-tea-ok'],
    entry_points={
        'console_scripts': [
            'request-tea-ok=main_module:make_request'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.20.0',
    ],
)
