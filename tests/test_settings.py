import os
import pprint
import random
import string
from datajoint import settings

__author__ = 'Fabian Sinz'

from nose.tools import assert_true, assert_raises, assert_equal, raises, assert_dict_equal
import datajoint as dj
import os

def test_load_save():
    """Testing load and save"""
    dj.config.save('tmp.json')
    conf = dj.Config()
    conf.load('tmp.json')
    assert_true(conf == dj.config, 'Two config files do not match.')
    os.remove('tmp.json')

def test_singleton():
    """Testing singleton property"""
    dj.config.save('tmp.json')
    conf = dj.Config()
    conf.load('tmp.json')
    conf['dummy.val'] = 2

    assert_true(conf == dj.config, 'Config does not behave like a singleton.')
    os.remove('tmp.json')

def test_singleton2():
    """Testing singleton property"""
    conf = dj.Config()
    conf['dummy.val'] = 2
    _ = dj.Config() # a new instance should not delete dummy.val
    assert_true(conf['dummy.val'] == 2, 'Config does not behave like a singleton.')



@raises(ValueError)
def test_nested_check():
    """Testing nested rejection"""
    dummy = {'dummy.testval': {'notallowed': 2}}
    dj.config.update(dummy)

@raises(dj.DataJointError)
def test_validator():
    """Testing validator"""
    dj.config['database.port'] = 'harbor'

def test_del():
    """Testing del"""
    dj.config['peter'] = 2
    assert_true('peter' in dj.config)
    del dj.config['peter']
    assert_true('peter' not in dj.config)

def test_len():
    """Testing len"""
    assert_equal(len(dj.config), len(dj.config._conf))

def test_str():
    """Testing str"""
    assert_equal(str(dj.config), pprint.pformat(dj.config._conf, indent=4))

def test_repr():
    """Testing repr"""
    assert_equal(repr(dj.config), pprint.pformat(dj.config._conf, indent=4))

@raises(ValueError)
def test_nested_check2():
    """Testing nested dictionary rejection"""
    dj.config['dummy'] = {'dummy2':2}

def test_save():
    """Testing save of config"""
    tmpfile = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
    moved = False
    if os.path.isfile(settings.LOCALCONFIG):
        os.rename(settings.LOCALCONFIG, tmpfile)
        moved = True
    dj.config.save()
    assert_true(os.path.isfile(settings.LOCALCONFIG))
    if moved:
        os.rename(tmpfile, settings.LOCALCONFIG)

def test_load_save():
    """Testing load and save of config"""
    filename_old = dj.settings.LOCALCONFIG
    filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(50)) + '.json'
    dj.settings.LOCALCONFIG = filename
    dj.config.save()
    dj.config.load(filename=filename)
    dj.settings.LOCALCONFIG = filename_old
    os.remove(filename)

def test_contextmanager():
    """Testing context manager"""
    dj.config['arbitrary.stuff'] = 7

    with dj.config(arbitrary__stuff=10) as cfg:
        assert_true(dj.config['arbitrary.stuff'] == 10)
    assert_true(dj.config['arbitrary.stuff'] == 7)

