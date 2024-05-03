if exist "dist" rmdir /s dist
python setup.py sdist
twine upload dist/* 
PAUSE