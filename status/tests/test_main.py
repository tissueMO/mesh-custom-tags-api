##########################################################################################
#   永続的に状態管理を行うAPIのテストコードです。
##########################################################################################
import pytest
import api.main as main

@pytest.mark.dependency()
def test_reset():
    assert isinstance(main.reset(), dict)

@pytest.mark.dependency(depends=["test_reset"])
def test_on():
    assert isinstance(main.on({
        "name": "medicine",
    }), dict)

@pytest.mark.dependency(depends=["test_on"])
def test_off():
    assert isinstance(main.off({
        "name": "medicine",
    }), dict)

@pytest.mark.dependency(depends=["test_off"])
def test_set():
    assert isinstance(main.set({
        "name": "medicine",
        "value": 10,
    }), dict)

@pytest.mark.dependency(depends=["test_set"])
def test_get_status():
    assert isinstance(main.get_status({
        "name": "medicine",
    }), dict)

@pytest.mark.dependency(depends=["test_reset"])
def test_get_latest():
    assert isinstance(main.get_latest({
        "name": "medicine",
    }), dict)

@pytest.mark.dependency(depends=["test_reset"])
def test_get_latest_span():
    assert isinstance(main.get_latest_span({
        "name": "medicine",
    }), dict)
