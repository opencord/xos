# Unit Tests

Unit tests in XOS are in an embrional stage and are implemented trough python `UnitTest` library while executed using `nosetests`.

## Run Unit Tests

_NOTE that the environment has been tested only on Mac OS X, but it shouldn't be hard to port it to other OS_

There still a step of manual steps you'll need to execute in order to execute Unit Tests:

**Setup a python Virtual Environment**
```
source scirpts/setup_venv
```

**Install the geoip library**
```
brew install geoip
```

**Compile xProto**
```
cp xos/genx/tool/Makefile xos/core/models/
cd xos/core/models
make PREFIX=../../genx
cd ../../../ (go back to the root)
```

**Install and run postgres**
```
brew install postgres
postgres -D /usr/local/var/postgres
```

**Execute Unit Tests**
```
XOS_ENV=test nosetests -s -vv  xos
```