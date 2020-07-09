# Overview

MariaDb Charm for Kubernetes using the Operator Framework.  
This charm provides the mysql interface for other charmed-osm charms.

# Usage

To use, first pull in dependencies via `git submodule`:

```
git submodule init
git submodule update
```

You must specify key configuration attributes when deploying,
or else arbitary defaults will be used. The attributes which
should be set are:

```
- user
- password
- database
- root_password
```

# Example
```
juju deploy . \
--config user=syed \
--config password=mohammad \
--config database=adnan \
--config root_password=karim
```
These values may also be in a config.yaml file, eg

```
$ juju deploy mysql --config config.yaml
```

Finally, deploy and relate a database:

```bash
juju deploy cs:~charmed-osm/keystone-k8s
juju relate mariadb-k8s keystone-k8s
```

**Charm structure:**

```
├── config.yaml
├── hooks
│   └── start -> ../src/charm.py
├── lib
│   ├── ops -> ../mod/operator/ops
├── metadata.yaml
├── mod
│   └── operator
│       ├── LICENSE.txt
│       ├── Makefile
│       ├── ops
│       │   ├── charm.py
│       │   ├── framework.py
│       │   ├── __init__.py
│       │   ├── jujuversion.py
│       │   ├── main.py
│       │   ├── model.py
│       ├── README.md
│       ├── setup.py
│       └── test
│           ├── bin
│           │   ├── relation-ids
│           │   └── relation-list
│           ├── charms
│           │   └── test_main
│           │       ├── config.yaml
│           │       ├── lib
│           │       │   ├── __init__.py
│           │       │   └── ops -> ../../../../ops
│           │       ├── metadata.yaml
│           │       └── src
│           │           └── charm.py
│           ├── __init__.py
│           ├── test_charm.py
│           ├── test_framework.py
│           ├── test_helpers.py
│           ├── test_jujuversion.py
│           ├── test_main.py
│           └── test_model.py
├── src
│   ├── charm.py
│   └── interface_mysql_provides.py
└── templates
    ├── README.md
    ├── spec_template_ha.yaml
    └── spec_template.yaml
```

# Development Guide

## Install Test Dependencies

1. Install pyenv so that you can test with different versions of Python

```
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
```

2. Append the following to your ~/.bashrc then log out and log back in

```
export PATH="/home/mark/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

3. Install development packages

```
sudo apt install build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git
```

4. Install Python 3.6.10 and 3.7.7

```
pyenv install 3.6.10
pyenv install 3.7.7
```

NOTE: For more available versions, run `pyenv install --list`

5. Create a virtualenv for this project

```
pyenv virtualenv 3.6.10 mariadb-3.6.10
```

Your newly created virtualenv should now be activated if your prompt change
to the following:

```
(mariadb-3.6.10) ubuntu@dev-18-04-2:~/src/mariadb-operator$
```

Notice the things in parentheses that corresponds to the virtualenv you created
in the previous step. This is thanks to the coordination of pyenv-virtualenv and
a `.python-version` file in the rootdir of this project.

If you `cd ..` or `cd` anywhere else the virtualenv will automatically be
deactivated. When you `cd` back into the project dir, the virtualenv will
automatically be activated.

6. Install more development dependencies:

```
python3 -m pip install --upgrade pip
python3 -m pip install "pip-tools>=5.2.1,<5.3"
pip-sync test-requirements.txt
```

7. Subsequent installation of development dependencies

```
pip-sync test-requirements.txt
```

## Adding A Test Dependency

1. Add it to `test-requirements.in` and then compile it:

```
echo "foo=>1.0.0,<1.1.0" >> test-requirements.in
pip-compile test-requirements.in
```

2. Sync the packages installed in your env to the ones declared
   in the regenerated `test-requirements.txt`

```
pip-sync test-requirements.txt
```

3. Commit `test-requirements.in` and `test-requirements.txt`. Both
   files should now be updated and the `foo` package installed in your
   local machine. Make sure to commit both files to the repo to let your
   teammates know of the new dependency.

```
git add test-requirements.*
git commit -m "Add foo to test-requirements.txt"
git push origin
```

## Running All The Tests

1. Ensure you start with a new terminal session because sometimes the shell
   won't find tox immediately after installation.

2. Run:

```
tox
```

## Viewing the Coverage Report

To view the coverage report, run the tests first and then run:

```
make coverage-server
```

This will run a simple web server on port 5000 that will serve the files
in the auto-generated `htmlcov/` directory. You may leave this server running
in a separate session as you run the tests so that you can just switch back
to the browser and hit refresh to see the changes to your coverage down to
the line of code.
