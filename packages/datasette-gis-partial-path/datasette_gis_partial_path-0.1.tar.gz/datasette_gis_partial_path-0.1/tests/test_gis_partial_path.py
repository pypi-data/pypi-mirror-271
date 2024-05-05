from datasette_gis_partial_path import prepare_connection
import sqlite3
import pytest

KD0FNR = 34.60406895585743,-106.40656400447672
N6MKW = 30.2528002,-81.72640779999999
el_lat = 34.60255892399174
el_lng = -106.38528612413097

@pytest.fixture
def conn():
    conn = sqlite3.connect(":memory:")
    prepare_connection(conn)
    return conn

@pytest.mark.parametrize("type", (float, str))
def test_gis_partial_path(conn, type):
    actual = conn.execute(
        "select gis_partial_path_lat(?, ?, ?, ?, ?)",
        [type(KD0FNR[0]), type(KD0FNR[1]), type(N6MKW[0]), type(N6MKW[1]), 2000],
    ).fetchall()[0][0]
    assert el_lat == pytest.approx(actual, rel=1e-2)
    actual = conn.execute(
        "select gis_partial_path_lng(?, ?, ?, ?, ?)",
        [type(KD0FNR[0]), type(KD0FNR[1]), type(N6MKW[0]), type(N6MKW[1]), 2000],
    ).fetchall()[0][0]
    assert el_lng == pytest.approx(actual, rel=1e-2)
