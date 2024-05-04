# Diamond

Created by following this guide: https://packaging.python.org/en/latest/tutorials/packaging-projects/

Note to self:
To push a new version, do the following:
- Update pyptoject.toml (make sure to change the version number!)
- Run `python -m build`
- Run `python -m twine upload dist/*`
