# Cloud Components

---
## Docs

Comming soon...

---
## Github Actions

---

#### Enviroment variables
- ``LINT_PATH``: This will be passed as a pararameter when have Pylint call 


#### Jobs
- ``test``: Do all tests using pylint
- ``lint``: Use Pylint to make this step
- ``deploy``: Deploy into pypi repository

---
## Makefile
This tool are used by Github Actions and can be used to debug or change some aspect into your CI/CD pipeline. Please do not change any rule name listed here! If that event happen, you need to change some make calls into Github Action configuration.

---
#### Tools
- ``test``: Run Pytest
- ``lint``: Run Pylint

#### Install
- ``install_pkg``: Intall everything, including Poetry and all dependencies from your project
- ``install_poetry``: Install only Poetry

#### Build
- ``build_src``: Build your package to deploy into Pypi repository