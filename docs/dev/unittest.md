# Unit Testing

XOS supports automated unit tests using the `nose2` unit testing framework.

## Setting up a unit testing environment

To run unit tests, an environment needs to be setup with the appropriate python
libraries used by the unit testing framework and by the XOS libraries that are
being tested. One way to accomplish this is to setup a
[virtual-env](local_env.md). You will also need to copy Chameleon from
`component/chameleon` to `containers/xos/tmp.chameleon`. Here is a set of
commands that may prove useful:

```shell
brew install graphviz
pip install --install-option="--include-path=/usr/local/include/" --install-option="--library-path=/usr/local/lib/" pygraphviz
source scripts/setup_venv.sh
pip install nose2 mock
cp -R ../../component/chameleon containers/xos/tmp.chameleon
```

## Running unit tests

To run unit tests, go to the root of the xos repository and run the following:

```shell
nose2 --verbose
```

## Writing new unit tests

New test filename should start with the string `test`. For example,
`test_mymodule.py`. If named properly, then `nose2` will automatically pick
them up.

## Ignoring unwanted unit tests

Some tests are still being migrated to the unit testing framework and/or
require features that may not be present in the virtual-env. Placing the
[__test__
attribute](https://nose2.readthedocs.io/en/latest/plugins/dundertests.html) set to `False`:

```python
__test__ = False
```

in a class will exclude it from being evaluated by the test framework.

