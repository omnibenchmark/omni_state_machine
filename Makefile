install:
	pipx install pipenv
	pipenv install -r requirements.txt
activate:
	pipenv shell
benchmark:
	snakemake -p --cores 1
dry:
	snakemake -p --cores 1 -n -p
