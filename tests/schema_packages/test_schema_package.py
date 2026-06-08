import os.path

from nomad.client import normalize_all, parse


def test_schema_package():
    test_file = os.path.join('tests', 'data', 'test.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    data = entry_archive.data

    assert data.full_name == 'Markus'
    assert data.email == 'markus@example.com'
    assert data.role_at_fairmat == 'Coordinator'
    assert data.fairmat_areas == ['F: Outreach']

    assert hasattr(data, 'summary')
    assert hasattr(data, 'total_expenses')
