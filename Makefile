.PHONY: help
help:
	@cat $(MAKEFILE_LIST) | grep -e "^[a-zA-Z_\-]*: *.*## *" | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

init: ## Initialise environment (one time action)
	pyenv virtualenv 3.7.4 zeppelin-to-html-3.7.4
	pyenv local zeppelin-to-html-3.7.4
	pip install --upgrade pip
	pip install -r requirements.txt

zep-to-html: ## Convert Zeppelin notebook (json file) to Html
	python zeppelin2Html.py $(zep)

html-to-pdf: ## Convert Html to pdf
	wkhtmltopdf $(html) $(basename $(html)).pdf

