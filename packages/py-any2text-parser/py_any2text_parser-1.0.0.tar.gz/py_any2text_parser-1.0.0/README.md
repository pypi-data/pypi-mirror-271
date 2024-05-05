# any2text-parser

## initialize

```shell
python3 -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
```

## test

```shell
python3 test_pdf2text.py
```

## usage

```python
from pdf2text.pdf2text import extract_pdf_file_to_text

file_path = "/Users/user/Downloads/AUDIT_MATERIALS/budget_materials/personal/2021/2021 03 remarks 2.pdf"
  
with open(file_path, "rb") as file:
  text_data, text = extract_pdf_file_to_text(
    filename="abc.pdf",
    file=file,
    meta_data_mapping = {
        "document_category": "DEF",
    }
  )
  
  print(text_data, text)
```
