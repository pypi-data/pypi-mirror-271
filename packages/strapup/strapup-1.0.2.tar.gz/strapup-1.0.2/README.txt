
Update pythonpath as need on startup of script. Create a custom logger, which can log to terminal and file at the same time, by simply choosing a name.

python3 -m build && python3 -m twine upload --verbose --skip-existing --repository pypi dist/*

# python3 -m twine upload --repository testpypi dist/*
# python3 -m twine upload --repository pypi dist/*

# python3 -m pip install --upgrade build
# python3 -m build

# python3 -m pip install --upgrade twine
# python3 -m twine upload --repository testpypi dist/*
# python3 -m twine upload --repository pypi dist/*
