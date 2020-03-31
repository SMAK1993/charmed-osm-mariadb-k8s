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
$ juju deploy . \
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

