list:
	@grep '^[^#[:space:]].*:' Makefile

# Build the python codebase
build:
	cd src/babbel-etl; \
	poetry build; \
	cd ..; \
	cd ..;
	
# Run unit test in python codebase
test:
	echo 'Not Implemented.'

# Deploy solution in Local Stack
deploy:
	localstack start -d; \
	cd infra/environment/local; \
	terraform apply; \
	cd ../../..;


