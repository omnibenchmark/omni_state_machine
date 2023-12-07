run:
	pipenv run jupyter-notebook OmniSpec.ipynb

shell:
	pipenv shell

update:
	pipenv install -r requirements.txt

install:
	pipx install pipenv

