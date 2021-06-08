import nose
import arrow
import acp_times

def test_open_300():
    assert str(acp_times.open_time(200, 300, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T05:53:00+00:00"
    assert str(acp_times.open_time(201, 300, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T05:55:00+00:00"
    assert str(acp_times.open_time(250, 300, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T07:27:00+00:00"
    assert str(acp_times.open_time(299, 300, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T08:59:00+00:00"
    assert str(acp_times.open_time(300, 300, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T09:00:00+00:00"
    assert str(acp_times.open_time(301, 300, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T09:00:00+00:00"

def test_close_300():
    assert str(acp_times.close_time(200, 300, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T13:20:00+00:00"
    assert str(acp_times.close_time(201, 300, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T13:24:00+00:00"
    assert str(acp_times.close_time(250, 300, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T16:40:00+00:00"
    assert str(acp_times.close_time(299, 300, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T19:56:00+00:00"
    assert str(acp_times.close_time(300, 300, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T20:00:00+00:00"
    assert str(acp_times.close_time(301, 300, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T20:00:00+00:00"
