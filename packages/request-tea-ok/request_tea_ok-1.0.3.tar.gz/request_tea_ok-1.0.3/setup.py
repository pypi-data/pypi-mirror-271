from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    author='Wahdalo',
    author_email='ahdx.wtf@gmail.com',
    name='request-tea-ok',
    version='1.0.3',
    description='This function is designed to make HTTP requests to the website app.tea.xyz',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['request_tea_ok'],
    url='https://github.com/wahdalo/tea-python',
    project_urls={
        'Homepage': 'https://github.com/wahdalo/tea-python',
        'Source': 'https://github.com/wahdalo/tea-python',
    },
    entry_points={
        'console_scripts': [
            'request_tea_ok=main_module:make_request'
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
