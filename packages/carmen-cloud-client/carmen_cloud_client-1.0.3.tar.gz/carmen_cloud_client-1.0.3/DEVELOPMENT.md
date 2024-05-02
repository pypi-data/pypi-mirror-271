```
pip install -r requirements.txt
pip install -r requirements-dev.txt

pip install datamodel-code-generator
./update-openapi-spec.sh
./generate-response.sh

python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build
python3 -m build
python3 -m pip install --upgrade twine
python3 -m twine upload --repository pypi dist/* # username: __token__, pw: API token (pypi-*)
```
