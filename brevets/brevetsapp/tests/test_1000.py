import nose
import arrow
import acp_times

def test_open_1000():
    assert str(acp_times.open_time(600, 1000, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T18:48:00+00:00"
    assert str(acp_times.open_time(601, 1000, arrow.get('2020-01-01T00:00:00'))) == "2020-01-01T18:50:00+00:00"
    assert str(acp_times.open_time(999, 1000, arrow.get('2020-01-01T00:00:00'))) == "2020-01-02T09:03:00+00:00"
    assert str(acp_times.open_time(1000, 1000, arrow.get('2020-01-01T00:00:00'))) == "2020-01-02T09:05:00+00:00"
    assert str(acp_times.open_time(1001, 1000, arrow.get('2020-01-01T00:00:00'))) == "2020-01-02T09:05:00+00:00"

def test_close_1000():
    assert str(acp_times.close_time(600, 1000, arrow.get('2020-01-01T00:00:00'))) == "2020-01-02T16:00:00+00:00"
    assert str(acp_times.close_time(601, 1000, arrow.get('2020-01-01T00:00:00'))) == "2020-01-02T16:05:00+00:00"
    assert str(acp_times.close_time(999, 1000, arrow.get('2020-01-01T00:00:00'))) == "2020-01-04T02:55:00+00:00"
    assert str(acp_times.close_time(1000, 1000, arrow.get('2020-01-01T00:00:00'))) == "2020-01-04T03:00:00+00:00"
    assert str(acp_times.close_time(1001, 1000, arrow.get('2020-01-01T00:00:00'))) == "2020-01-04T03:00:00+00:00"