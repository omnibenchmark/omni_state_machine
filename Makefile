install:
	pipx install pipenv
	pipenv install -r requirements.txt
activate:
	pipenv shell
benchmark:
	snakemake -p --cores 1
dry:
	snakemake -p --cores 1 -n -p -F
clean:
	rm -rf ./out ./log
wild:
	snakemake -s test_wildcard_constrains.snmk -p --cores 1
