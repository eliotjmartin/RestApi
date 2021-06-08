import nose
import arrow
import acp_times

def test_open_under_60():
    assert str(acp_times.open_time(0, 200, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T00:00:00+00:00"
    assert str(acp_times.open_time(10, 200, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T00:18:00+00:00"
    assert str(acp_times.open_time(34, 200, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T01:00:00+00:00"
    assert str(acp_times.open_time(59, 200, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T01:44:00+00:00"

def test_close_under_60():
    assert str(acp_times.close_time(0, 200, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T01:00:00+00:00"
    assert str(acp_times.close_time(10, 200, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T01:30:00+00:00"
    assert str(acp_times.close_time(34, 200, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T02:42:00+00:00"
    assert str(acp_times.close_time(59, 200, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T03:57:00+00:00"

def test_open_over_60():
    assert str(acp_times.open_time(60, 200, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T01:46:00+00:00"
    assert str(acp_times.open_time(61, 200, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T01:48:00+00:00"
    assert str(acp_times.open_time(100, 200, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T02:56:00+00:00"
    assert str(acp_times.open_time(199, 200, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T05:51:00+00:00"
    assert str(acp_times.open_time(200, 200, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T05:53:00+00:00"
    assert str(acp_times.open_time(206, 200, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T05:53:00+00:00"


def test_close_over_60():
    assert str(acp_times.close_time(60, 200, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T04:00:00+00:00"
    assert str(acp_times.close_time(61, 200, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T04:04:00+00:00"
    assert str(acp_times.close_time(100, 200, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T06:40:00+00:00"
    assert str(acp_times.close_time(199, 200, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T13:16:00+00:00"
    assert str(acp_times.close_time(200, 200, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T13:30:00+00:00"
    assert str(acp_times.close_time(206, 200, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T13:30:00+00:00"
