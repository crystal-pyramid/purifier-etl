include .env
export

all:
	@echo "GOOGLE_APPLICATION_CREDENTIALS is $(GOOGLE_APPLICATION_CREDENTIALS)"

local:
	python crypt_pipeline.py --DirectRunner --bucket=$(BUCKET_NAME) --project=$(PROJECT)

dataflow:
	python crypt_pipeline.py --DataFlowRunner --bucket=$(BUCKET_NAME) --project=$(PROJECT) 