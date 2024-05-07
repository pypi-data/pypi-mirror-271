import archive_ops.api as ao_api


def test_get_archive_location_alpha():
    work_name = "no-numbers"
    base = "parent"
    expected = f"{base}0/00/{work_name}"
    actual = ao_api.get_archive_location(base, work_name)
    assert actual == expected

def test_get_archive_location_numeric():
    work_name = "W1FPL2251"
    base = "parent"
    expected = f"{base}1/51/{work_name}"
    actual = ao_api.get_archive_location(base, work_name)
    assert actual == expected


def test_get_s3_location():
    work_name = "W1FPL2251"
    base = "parent"
    expected = f"{base}/8d/{work_name}"
    actual = ao_api.get_s3_location(base, work_name)
    assert actual == expected


def test_get_buda_ig_from_disk_same():
    expected = 'flegel'
    actual = ao_api.get_buda_ig_from_disk('flegel')
    assert actual == expected


def test_get_buda_ig_from_disk_diff():
    disk_folder = '1234'
    expected = f"I{disk_folder}"
    actual = ao_api.get_buda_ig_from_disk(disk_folder)
    assert actual == expected


def test_get_disk_ig_from_buda_same():
    expected = 'flegel'
    actual = ao_api.get_disk_ig_from_buda('flegel')
    assert actual == expected


def test_get_disk_ig_from_buda_diff():
    expected = '1234'
    nn = ao_api.get_disk_ig_from_buda(f"I{expected}")
    assert nn == expected
