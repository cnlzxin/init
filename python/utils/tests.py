from .tools import extract_data_structure as extract


def test_extract_data_structure_tools():
    assert extract(False) == extract(True)
    assert extract(None) != extract(False)

    assert extract(1) == extract(2)
    assert extract('a') == extract('b')

    # list
    assert extract([]) == extract([])
    assert extract([1, 2]) == extract([3, 4])

    # dict
    assert extract({}) == extract({})
    assert extract({'key': 'value'}) == extract({'key': 'data'})
    assert extract({'key': 'value'}) != extract({'field': 'data'})

    # nest
    left_test_data = {
        'key': 'value',
        'hello': [{'ip': '192.168.1.1', 'port': 102, 'is_active': False}]
    }
    right_test_data = {
        'key': 'data',
        'hello': [{'ip': '192.168.1.2', 'port': 502, 'is_active': False}]
    }
    assert extract(left_test_data) == extract(right_test_data)
