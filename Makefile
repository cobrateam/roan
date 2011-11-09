bootstrap:
	@pip install -r requirements.txt

clean:
	@git clean -dfX

test: clean
	@nostests --with-django --django-sqlite --django-settings=settings_test --with-coverage --cover-packages=roan --cover-erase
