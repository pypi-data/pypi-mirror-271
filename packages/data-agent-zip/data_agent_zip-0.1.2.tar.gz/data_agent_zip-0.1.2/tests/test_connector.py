import numpy as np
import pandas as pd


def test_sanity(zip_archive):
    assert zip_archive.connected
    zip_archive.disconnect()
    assert not zip_archive.connected
    zip_archive.connect()
    assert zip_archive.connected

    group_name = "test_group.csv"

    info = zip_archive.connection_info()
    assert "Path" in info and info["Path"]

    assert zip_archive.list_groups() == []

    df = pd.DataFrame(
        np.random.randint(0, 10**4, size=(10**4, 4)),
        columns=list("ABCD"),
        index=pd.date_range("1980-01-01", freq="19S", periods=10**4),
    )
    df.index.name = "timestamp"

    zip_archive.write_group_values_period(group_name, df)

    tags = zip_archive.list_tags()

    assert tags[group_name]["Name"] == "test_group.csv"
    assert tags[group_name]["FileSize"] > 200000
    assert tags[group_name]["HasChildren"] is True

    zip_archive.list_groups() == ["test_group.csv"]

    df1 = zip_archive.read_group_values_period(group_name)
    pd.testing.assert_frame_equal(df1, df, check_freq=False, check_dtype=False)

    df2 = zip_archive.read_tag_values_period(["test_group.csv::B", "test_group.csv::D"])
    pd.testing.assert_frame_equal(
        df2, df[["B", "D"]], check_freq=False, check_dtype=False
    )

    details = zip_archive.group_details(
        group_name, include_range=True, include_rowcount=True
    )
    assert "FileSize" in details and details["FileSize"] > 0

    assert zip_archive.list_tags(group_name) == {
        "test_group.csv::A": {"Name": "A", "HasChildren": False},
        "test_group.csv::B": {"Name": "B", "HasChildren": False},
        "test_group.csv::C": {"Name": "C", "HasChildren": False},
        "test_group.csv::D": {"Name": "D", "HasChildren": False},
    }

    res = zip_archive.list_tags(group_name, include_attributes=True)
    assert res["test_group.csv::A"]["FirstTimestamp"] == "1980-01-01 00:00:00"
    assert res["test_group.csv::A"]["LastTimestamp"] == "1980-01-03 04:46:21"
    assert res["test_group.csv::A"]["TotalRows"] == 10**4
    assert len(res) == 4

    res = zip_archive.list_tags(group_name, include_attributes=True, max_results=2)
    assert len(res) == 2


def test_append_similar(zip_archive):
    group_name = "test_group.csv"

    df1 = pd.DataFrame(
        np.random.randint(0, 100, size=(100, 4)),
        columns=list("ABCD"),
        index=pd.date_range("1980-01-01", freq="19S", periods=100),
    )
    df1.index.name = "timestamp"

    df2 = pd.DataFrame(
        np.random.randint(0, 100, size=(100, 4)),
        columns=list("ABCD"),
        index=pd.date_range("1980-01-01", freq="19S", periods=100),
    )
    df2.index.name = "timestamp"

    zip_archive.write_group_values_period(group_name, df1, on_conflict="ignore")
    df_res = zip_archive.read_group_values_period(group_name)
    pd.testing.assert_frame_equal(df1, df_res, check_freq=False, check_dtype=False)

    zip_archive.write_group_values_period(group_name, df2, on_conflict="append")
    df_res = zip_archive.read_group_values_period(group_name)
    # assert len(df_res) == 100 * 2

    # res = zip_archive.list_tags(group_name, include_attributes=True)
    # assert list(res.keys()) == [
    #     "test_group.csv::A",
    #     "test_group.csv::B",
    #     "test_group.csv::C",
    #     "test_group.csv::D",
    # ]


# def test_append_different(zip_archive):
#     group_name = "test_group.csv"
#
#     df1 = pd.DataFrame(
#         np.random.randint(0, 100, size=(100, 4)),
#         columns=list("DCBA"),
#         index=pd.date_range("1980-01-01", freq="19S", periods=100),
#     )
#     df1.index.name = "timestamp"
#
#     df2 = pd.DataFrame(
#         np.random.randint(0, 100, size=(100, 2)),
#         columns=list("EF"),
#         index=pd.date_range("1980-01-01", freq="19S", periods=100),
#     )
#     df2.index.name = "timestamp"
#
#     df3 = pd.DataFrame(
#         np.random.randint(0, 100, size=(100, 4)),
#         columns=list("ACDB"),
#         index=pd.date_range("1980-01-01", freq="19S", periods=100),
#     )
#     df3.index.name = "timestamp"
#
#     csv_store.write_group_values_period(group_name, df1, on_conflict="override")
#     df_res = csv_store.read_group_values_period(group_name)
#     pd.testing.assert_frame_equal(df1, df_res, check_freq=False, check_dtype=False)
#
#     with pytest.raises(Exception):
#         csv_store.write_group_values_period(group_name, df2, on_conflict="append")
#
#     csv_store.write_group_values_period(group_name, df3, on_conflict="append")
#     df_res = csv_store.read_group_values_period(group_name)
#     assert len(df_res) == 100 * 2


def test_write_tag_attributes(zip_archive):
    attr = {
        "tag1": {"Name": "Tag 1", "Type": "bool"},
        "tag2": {"Name": "Tag 2", "Type": "int", "non_standard": 0},
        "tag23": {
            "Name": "Tag 23",
            "Type": "double",
            "Description": "Non interesting tag",
        },
    }

    zip_archive.write_tag_attributes(attr)

    attr = {
        "tag1": {"Name": "Tag 1", "Type": "bool"},
        "group::tag2": {"Name": "Tag 2", "Type": "int"},
        "group::tag23": {"Name": "Tag 23", "Type": "double"},
        "quote": {"Name": "Quote(,)", "Type": "str"},
    }

    zip_archive.write_tag_attributes(attr)
