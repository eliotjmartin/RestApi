import nose
import arrow
import acp_times

def test_open_400():
    assert str(acp_times.open_time(300, 400, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T09:00:00+00:00"
    assert str(acp_times.open_time(301, 400, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T09:02:00+00:00"
    assert str(acp_times.open_time(399, 400, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T12:06:00+00:00"
    assert str(acp_times.open_time(400, 400, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T12:08:00+00:00"
    assert str(acp_times.open_time(401, 400, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T12:08:00+00:00"

def test_close_400():
    assert str(acp_times.close_time(300, 400, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T20:00:00+00:00"
    assert str(acp_times.close_time(301, 400, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T20:04:00+00:00"
    assert str(acp_times.close_time(399, 400, arrow.get('2020-01-01T00:00:00'))) == "2020-01-02T02:36:00+00:00"
    assert str(acp_times.close_time(400, 400, arrow.get('2020-01-01T00:00:00'))) == "2020-01-02T03:00:00+00:00"
    assert str(acp_times.close_time(401, 400, arrow.get('2020-01-01T00:00:00'))) == "2020-01-02T03:00:00+00:00"