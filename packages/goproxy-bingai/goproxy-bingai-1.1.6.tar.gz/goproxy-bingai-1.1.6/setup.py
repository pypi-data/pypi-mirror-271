from setuptools import setup, find_packages

setup(
    name='goproxy-bingai',
    version='1.1.6',
    description='Microsoft Login Lib',
    url='https://github.com/shoot82003/goproxy_bingai',
    author='shoot82003',
    author_email='shoot82003@qq.com',
    packages=find_packages(),
    package_data={'goproxy_bingai':['*.so','*.dll']},
    platforms=['linux', 'windows', 'macos'],
    classifiers=[
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3',
    ],
)