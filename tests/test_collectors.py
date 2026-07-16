from exporter.collectors import SystemSnapshot, collect_system_snapshot


def test_collect_system_snapshot_returns_valid_ranges():
    snapshot = collect_system_snapshot()

    assert isinstance(snapshot, SystemSnapshot)
    assert 0.0 <= snapshot.cpu_percent <= 100.0
    assert 0.0 <= snapshot.memory_percent <= 100.0
    assert snapshot.memory_used_bytes <= snapshot.memory_total_bytes
    assert snapshot.load_avg_1m >= 0.0
    assert snapshot.process_count > 0


def test_collect_system_snapshot_disks_have_valid_percent():
    snapshot = collect_system_snapshot()

    for disk in snapshot.disks:
        assert 0.0 <= disk.percent <= 100.0
        assert disk.used_bytes <= disk.total_bytes + 1  # tolerate rounding
        assert disk.mountpoint


def test_collect_system_snapshot_network_counters_are_non_negative():
    snapshot = collect_system_snapshot()

    assert snapshot.net_bytes_sent >= 0
    assert snapshot.net_bytes_recv >= 0
