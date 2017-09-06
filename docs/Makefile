swagger: swagger_clean swagger_docs swagger_serve_spec

swagger_docs:
	python scripts/swagger_docs.py

swagger_clean:
	rm -r swagger/specs/*

swagger_serve_spec:
	@echo $(CWD)
	http-server --cors ./swagger
