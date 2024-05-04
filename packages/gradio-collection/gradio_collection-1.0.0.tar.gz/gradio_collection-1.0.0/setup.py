from setuptools import setup, find_packages

setup(
    name='gradio_collection',
    version='1.0.0',
    author='Daniel Ialcin Misser Westergaard',
    description='A collection of Custom Gradio components.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dwancin/gradio-collection/',
    keywords=['gradio', 'gradio-custom-component', 'meta-package'],
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.6',
    install_requires=[
        'gradio>=4.0,<5.0',
        'gradio-toggle',
        'gradio-grid',
        'gradio-imagefeed',
        'gradio-highlightedcode',
        'gradio-modal',
        'gradio-pdf',
        'gradio-calendar',
        'gradio-imageslider',
        'gradio_folium',
        'gradio-notebook'
    ],
    include_package_data=True
)
