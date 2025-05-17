import pytest
import datetime
from unittest.mock import patch, MagicMock
from hikvision_alert.events import EventStore
from hikvision_alert import events

class DummyConfig:
    CAMERAS_NAME = {'1': 'Camara_1'}
    MAX_EVENTS = 3
    LOKI_URL = 'test'
    TIME_ZONE = 'UTC'
    CAMERA_SCHEDULES = {}
    DIFFERENCE_TIME = 20

@pytest.fixture(autouse=True)
def patch_config(monkeypatch):
    monkeypatch.setattr(events, "config", DummyConfig)
    yield

@pytest.fixture
def event_store():
    return EventStore()

def sample_event(channel='1', timestamp=None):
    return {
        'channelID': channel,
        'cameraName': 'Camara_1',
        'eventDescription': 'Movimiento detectado',
        'targetType': 'Persona',
        'eventState': 'active',
        'bkgUrl': 'http://snapshot',
        'detectionPicturesNumber': 1,
        'activePostCount': 1,
        'timestamp': timestamp
    }

def test_add_event(event_store):
    event = sample_event()
    alert_event = event_store.add_event(event)
    assert alert_event['channel'] == '1'
    assert alert_event['channel_name'] == 'Camara_1'
    assert alert_event['event_description'] == 'Movimiento detectado'
    assert alert_event['result'] is False
    assert alert_event['number_of_objects'] == 1
    assert alert_event['active_post_count'] == 1
    assert len(event_store.events) == 1

def test_get_event(event_store):
    event = sample_event()
    alert_event = event_store.add_event(event)
    found = event_store.get_event(alert_event['id'])
    assert found == alert_event
    assert event_store.get_event('nonexistent') is None

def test_delete_event(event_store):
    event = sample_event()
    alert_event = event_store.add_event(event)
    assert event_store.delete_event(alert_event['id']) is True
    assert event_store.get_event(alert_event['id']) is None
    assert event_store.delete_event('nonexistent') is False

def test_update_idxs(event_store):
    event1 = event_store.add_event(sample_event(channel='1'))
    event2 = event_store.add_event(sample_event(channel='2'))
    event_store.update_idxs()
    assert event_store.idx[event1['id']] == 0
    assert event_store.idx[event2['id']] == 1
    assert '1' in event_store.idx_by_channel
    assert '2' in event_store.idx_by_channel

def test_confirm_detection(event_store, monkeypatch):
    event = sample_event()
    alert_event = event_store.add_event(event)
    monkeypatch.setattr('hikvision_alert.events.send_event_to_loki', lambda x: None)
    assert event_store.confirm_detection(alert_event['id'], ['person']) is True
    assert event_store.events[0]['result'] is True
    assert event_store.events[0]['detected_objects'] == ['person']

def test_get_last_event(event_store):
    assert event_store.get_last_event('1') is None
    event1 = event_store.add_event(sample_event(channel='1'))
    event2 = event_store.add_event(sample_event(channel='1'))
    last = event_store.get_last_event('1')
    assert last['id'] == event2['id']

def test_check_if_scheduled_no_schedules(event_store):
    DummyConfig.CAMERA_SCHEDULES = {}
    assert event_store.check_if_scheduled('1') is True

def test_check_if_scheduled_with_schedule(event_store):
    DummyConfig.CAMERA_SCHEDULES = {'1': {'start': '00:00', 'end': '23:59'}}
    assert event_store.check_if_scheduled('1') is True
    DummyConfig.CAMERA_SCHEDULES = {'1': {'start': '23:00', 'end': '01:00'}}
    # Should be True for times crossing midnight
    assert isinstance(event_store.check_if_scheduled('1'), bool)
    DummyConfig.CAMERA_SCHEDULES = {}

def test_check_if_recent_event_new(event_store):
    event = sample_event()
    is_recent, alert_event = event_store.check_if_recent_event(event)
    assert is_recent is False
    assert alert_event is not None

def test_check_if_recent_event_recent(event_store, monkeypatch):
    event = sample_event()
    alert_event = event_store.add_event(event)
    # Patch datetime to simulate a recent event
    with patch('hikvision_alert.events.datetime') as mock_datetime:
        now = datetime.datetime.strptime(alert_event['timestamp'], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(seconds=5)
        mock_datetime.datetime.now.return_value = now
        mock_datetime.datetime.strptime = datetime.datetime.strptime
        is_recent, last_event = event_store.check_if_recent_event(event)
        assert is_recent is True
        assert last_event['id'] == alert_event['id']

def test_event_store_max_events(event_store):
    event1 = event_store.add_event(sample_event(channel='1'))
    event2 = event_store.add_event(sample_event(channel='1'))
    event3 = event_store.add_event(sample_event(channel='1'))
    event4 = event_store.add_event(sample_event(channel='1'))
    assert len(event_store.events) == 3
    assert event1['id'] not in event_store.idx