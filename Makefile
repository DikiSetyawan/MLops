install : 
	pip install -r requirements.txt

run : 
	python testHello.py

lint : 
	pylint --disable=R, C hello.py

test : 
	python -m pytest -vv --cov-hello test_hello.py
	