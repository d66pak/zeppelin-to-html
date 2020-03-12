# Zeppelin Notebook to Html

This is a Python script to convert Zeppelin notebooks (json files) to Html format. The script uses Pygments for html conversion. Html files can later be converted to pdf format using **wkhtmltopdf**

## How to run

- `make help` for more info
- `make init` One time environment setup
- `make zep-to-html zep=MyNotebook.json` Convert Zeppelin notebook (json file) to Html
- `make html-to-pdf html=MyNotebook.html` Convert Html to pdf format