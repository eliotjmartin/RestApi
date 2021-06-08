import nose
import arrow
import acp_times

def test_open_600():
    assert str(acp_times.open_time(400, 600, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T12:08:00+00:00"
    assert str(acp_times.open_time(401, 600, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T12:10:00+00:00"
    assert str(acp_times.open_time(599, 600, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T18:46:00+00:00"
    assert str(acp_times.open_time(600, 600, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T18:48:00+00:00"
    assert str(acp_times.open_time(601, 600, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T18:48:00+00:00"

def test_close_600():
    assert str(acp_times.close_time(400, 600, arrow.get('2020-01-01T00:00:00'))) == "2020-01-02T02:40:00+00:00"
    assert str(acp_times.close_time(401, 600, arrow.get('2020-01-01T00:00:00'))) == "2020-01-02T02:44:00+00:00"
    assert str(acp_times.close_time(599, 600, arrow.get('2020-01-01T00:00:00'))) == "2020-01-02T15:56:00+00:00"
    assert str(acp_times.close_time(600, 600, arrow.get('2020-01-01T00:00:00'))) == "2020-01-02T16:00:00+00:00"
    assert str(acp_times.close_time(601, 600, arrow.get('2020-01-01T00:00:00'))) == "2020-01-02T16:00:00+00:00"