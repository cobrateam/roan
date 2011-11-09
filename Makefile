bootstrap:
	@pip install -r requirements.txt

clean:
	@git clean -dfX

test: clean
	@nosetests -s --with-django --django-settings=settings_test --with-coverage --cover-package=roan --cover-erase
