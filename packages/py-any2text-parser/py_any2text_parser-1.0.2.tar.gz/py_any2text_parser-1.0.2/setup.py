from setuptools import setup

setup(
    name='py_any2text_parser',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'pypinyin==0.51.0',
        'werkzeug==3.0.2',
        'pdf2image==1.17.0',
        'img2table==1.2.11',
        'requests==2.31.0',
        'unstructured==0.11.8',
        'sentence_transformers==2.7.0',
        'pdfminer==20191125',
        'pdfminer.six==20231228',
        'unstructured_inference==0.7.29',
        'pikepdf==8.15.1',
        'opencv-python==4.8.1.78',
        'opencv-contrib-python==4.8.1.78',
    ],
)
