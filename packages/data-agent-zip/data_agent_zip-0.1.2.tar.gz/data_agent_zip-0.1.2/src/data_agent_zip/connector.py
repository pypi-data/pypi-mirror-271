import csv
import io
import logging
import os
import tempfile
import zipfile
from functools import wraps
from typing import Union

import pandas as pd
from data_agent.abstract_connector import (
    STANDARD_ATTRIBUTES,
    AbstractConnector,
    SupportedOperation,
    active_connection,
    group_exists,
)

__author__ = "Meir Tseitlin"

log = logging.getLogger(f"ia_plugin.{__name__}")


def csv_file_extension_validate(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        if not args[0].lower().endswith(".csv"):
            args = list(args)
            args[0] = f"{str(args[0])}.csv"

        return func(self, *args, **kwargs)

    return inner


class ZipConnector(AbstractConnector):
    TYPE = "zip"
    CATEGORY = "archive"
    SUPPORTED_FILTERS = []
    SUPPORTED_OPERATIONS = [
        SupportedOperation.READ_TAG_PERIOD,
        SupportedOperation.WRITE_TAG_PERIOD,
        SupportedOperation.WRITE_TAG_META,
    ]
    DEFAULT_ATTRIBUTES = [
        ("Name", {"Type": "str", "Name": "Tag Name"}),
        ("engunits", {"Type": "str", "Name": "Units"}),
        ("descriptor", {"Type": "str", "Name": "Description"}),
        ("FirstTimestamp", {"Type": "str", "Name": "First Timestamp"}),
        ("FirstValue", {"Type": "int", "Name": "First Value"}),
        ("LastTimestamp", {"Type": "int", "Name": "Last Timestamp"}),
        ("LastValue", {"Type": "int", "Name": "Last Value"}),
        ("TotalRows", {"Type": "int", "Name": "Total Rows"}),
        ("FileSize", {"Type": "int", "Name": "File Size"}),
    ]

    TIMESTAMP_COL = "timestamp"
    SYSTEM_COLUMNS = [TIMESTAMP_COL]
    GROUP_DELIMITER = "::"
    DATA_FOLDER = "data"
    META_FOLDER = "meta"
    TAGS_LIST_FILE = "tags_list.csv"

    def __init__(self, conn_name="zip_archive", zipfile_path=None):
        super(ZipConnector, self).__init__(conn_name)

        self._zipfile_path = zipfile_path
        self._zipfile = None
        if self._zipfile_path is None:
            self._zipfile_path = os.path.join(
                tempfile.gettempdir(), f"{os.urandom(10).hex()}.zip"
            )
        self._tags_list_file = None

        log.debug(f"ZIP file path - {self._zipfile_path}")
        print(f"ZIP file path - {self._zipfile_path}")

    @staticmethod
    def list_connection_fields():
        return {
            "zipfile_path": {
                "name": "ZIP File",
                "type": "local_file",
                "default_value": "c:\\temp\\data.zip",
                "optional": False,
            }
        }

    @staticmethod
    def target_info(target_ref):
        return {}

    @property
    def connected(self):
        return self._zipfile is not None

    def connect(self):
        self._zipfile = zipfile.ZipFile(
            self._zipfile_path, mode="a", compression=zipfile.ZIP_DEFLATED
        )

        # Start tags list df
        self._tags_list_df = pd.DataFrame(columns=list(STANDARD_ATTRIBUTES.keys()))

        # Not available until Python 3.11
        # self._zipfile.mkdir(self.DATA_FOLDER)
        # self._zipfile.mkdir(self.META_FOLDER)

    @active_connection
    def disconnect(self):
        if self._zipfile:
            try:
                tags_list_file = self._zipfile.getinfo(self.TAGS_LIST_FILE)
            except KeyError:
                tags_list_file = zipfile.ZipInfo(self.TAGS_LIST_FILE)

            # Write tags list
            self._zipfile.writestr(
                tags_list_file, self._tags_list_df.to_csv(index=False)
            )

            self._zipfile.close()
            self._zipfile = None

    @active_connection
    def connection_info(self):
        return {
            "OneLiner": f"[{self.TYPE}] {self._zipfile_path}",
            "Path": self._zipfile_path,
        }

    @active_connection
    def list_tags(
        self,
        filter: Union[str, list] = "",
        include_attributes: Union[bool, list] = False,
        recursive: bool = False,
        max_results: int = 0,
    ):
        if max_results == 0:
            max_results = 2**32

        if filter == "":
            return {
                os.path.basename(g.filename): {
                    "Name": os.path.basename(g.filename),
                    "FileSize": g.file_size,
                    "CompressSize": g.compress_size,
                    "HasChildren": True,
                }
                for g in self._zipfile.infolist()
                if g.filename.endswith(".csv")
                and g.filename.startswith(self.DATA_FOLDER)
            }

        elif filter.endswith(".csv"):
            fqn = f"{self.DATA_FOLDER}/{filter}"

            with self._zipfile.open(fqn, "r") as csv_file:
                csv_reader = csv.DictReader(
                    io.TextIOWrapper(csv_file, newline=""), delimiter=","
                )

                total_rows = 0

                # Read first row
                first_row = {}
                for row in csv_reader:
                    # adding the first row (containing header)
                    first_row = row
                    break

                if not first_row:
                    return {}

                if include_attributes:
                    # Read last row
                    last_row = {}
                    for total_rows, row in enumerate(csv_reader, start=2):
                        last_row = row

                    if not last_row:
                        last_row = first_row

                    # return first_row
                    return {
                        f"{filter}{self.GROUP_DELIMITER}{col}": {
                            "Name": col,
                            "HasChildren": False,
                            "FirstTimestamp": first_row[self.TIMESTAMP_COL],
                            "FirstValue": first_row[col],
                            "LastTimestamp": last_row[self.TIMESTAMP_COL],
                            "LastValue": last_row[col],
                            "TotalRows": total_rows,
                        }
                        for _, col in zip(
                            range(max_results + len(self.SYSTEM_COLUMNS)), first_row
                        )
                        if col not in self.SYSTEM_COLUMNS
                    }
                else:
                    return {
                        f"{filter}{self.GROUP_DELIMITER}{col}": {
                            "Name": col,
                            "HasChildren": False,
                        }
                        for _, col in zip(
                            range(max_results + len(self.SYSTEM_COLUMNS)), first_row
                        )
                        if col not in self.SYSTEM_COLUMNS
                    }

    @active_connection
    @csv_file_extension_validate
    def group_details(self, group_name, include_range=False, include_rowcount=False):
        fqn = f"{self.DATA_FOLDER}/{group_name}"
        info = self._zipfile.getinfo(fqn)

        ret = {"FileSize": info.file_size}

        if include_range:
            ret["start_timestamp"] = None
            ret["end_timestamp"] = None

        if include_rowcount:
            ret["row_count"] = None

        return ret

    @active_connection
    def read_tag_attributes(self, tags: list, attributes: list = None):
        pass

    @active_connection
    def write_tag_attributes(self, tags: dict):
        # Group by CSV files
        groups = self._group_tags_by_csv_file(tags)

        for group in groups:
            df = pd.DataFrame.from_records(groups[group])
            df.index.name = "attribute"

            fqn = f"{self.META_FOLDER}/{group}.csv"

            try:
                zip_info = self._zipfile.getinfo(fqn)
            except KeyError:
                zip_info = zipfile.ZipInfo(fqn)

            self._zipfile.writestr(zip_info, df.to_csv())

        # Add standard attrs to df
        for tag in tags:
            self._tags_list_df.loc[len(self._tags_list_df.index)] = [
                tags[tag][a] if a in tags[tag] else None
                for a in STANDARD_ATTRIBUTES.keys()
            ]

            # row = ','.join([tags[tag][a] if a in tags[tag] else '' for a in STANDARD_ATTRIBUTES.keys()])

            # with self._zipfile.open(self.TAGS_LIST_FILE, "w") as fl:
            #     fl.write(row.encode())
            # self._zipfile.writestr(self._tags_list_file, df.to_csv(index=False))

    @active_connection
    def read_tag_values(self, tags: list):
        return pd.read_csv(self._path, index_col=self.TIMESTAMP_COL, usecols=tags)

    @active_connection
    def read_tag_values_period(
        self,
        tags: list,
        first_timestamp=None,
        last_timestamp=None,
        result_format="dataframe",
        progress_callback=None,
    ):
        groups = self._group_tags_by_csv_file(tags)

        data = []

        for group in groups:
            fqn = f"{self.DATA_FOLDER}/{group}"

            df = pd.read_csv(
                self._zipfile.open(fqn),
                index_col=self.TIMESTAMP_COL,
                usecols=groups[group] + [self.TIMESTAMP_COL] if groups[group] else None,
                parse_dates=True,
            )

            data.append(df)

        df = pd.concat(data, axis=1, sort=True)
        df.index.name = self.TIMESTAMP_COL
        return df

    @active_connection
    def write_tag_values(self, tags: dict, wait_for_result: bool = True, **kwargs):
        pass

    @active_connection
    @csv_file_extension_validate
    def write_tag_values_period(self, group_name, df, attributes=None):
        pass

    @active_connection
    def list_groups(self) -> list:
        return [
            os.path.basename(g)
            for g in self._zipfile.namelist()
            if g.endswith("csv") and os.path.dirname(g) == self.DATA_FOLDER
        ]

    @csv_file_extension_validate
    def group_period(self, group_name):
        pass

    @active_connection
    @csv_file_extension_validate
    def register_group(self, group_name: str, tags: list, refresh_rate_ms: bool = 1000):
        pass

    @active_connection
    @csv_file_extension_validate
    @group_exists
    def unregister_group(self, group_name: str):
        os.remove(os.path.join(self._path, group_name))

    @active_connection
    @csv_file_extension_validate
    @group_exists
    def read_group_values(self, group_name: str, from_cache: bool = True) -> dict:
        tags = self._groups[group_name]
        return self.read_tag_values(tags)

    @active_connection
    @csv_file_extension_validate
    def write_group_values(
        self, group_name: str, tags: dict, wait_for_result: bool = True, **kwargs
    ) -> dict:
        # df.to_csv(os.path.join(self._path, )
        pass

    @active_connection
    @csv_file_extension_validate
    @group_exists
    def read_group_values_period(
        self,
        group_name: str,
        first_timestamp=None,
        last_timestamp=None,
        from_cache: bool = True,
    ) -> dict:
        # print(os.path.join(self.DATA_FOLDER,group_name))
        fqn = f"{self.DATA_FOLDER}/{group_name}"

        df = pd.read_csv(
            self._zipfile.open(fqn),
            index_col=self.TIMESTAMP_COL,
            parse_dates=True,
        )
        return df

    @active_connection
    @csv_file_extension_validate
    def write_group_values_period(
        self,
        group_name: str,
        df: pd.DataFrame,
        wait_for_result: bool = True,
        on_conflict="append",
        **kwargs,
    ) -> dict:
        # assert on_conflict in ['raise', 'ignore', 'override', 'merge', 'append']
        assert on_conflict in ["append", "ignore"]

        fqn = f"{self.DATA_FOLDER}/{group_name}"

        try:
            zip_info = self._zipfile.getinfo(fqn)
        except KeyError:
            zip_info = None

        if on_conflict == "append":
            if not zip_info:
                zip_info = zipfile.ZipInfo(fqn)
            self._zipfile.writestr(zip_info, df.to_csv())

        elif on_conflict == "ignore" and zip_info is None:
            zip_info = zipfile.ZipInfo(fqn)
            self._zipfile.writestr(zip_info, df.to_csv())

    def _group_tags_by_csv_file(self, tags):
        groups = {}
        for tag in tags:
            tag_split = tag.rsplit(self.GROUP_DELIMITER)
            groups.setdefault(tag_split[0], {} if isinstance(tags, dict) else [])
            tag_short_name = (
                tag_split[1] if self.GROUP_DELIMITER in tag else tag_split[0]
            )
            if isinstance(tags, dict):
                groups[tag_split[0]][tag_short_name] = tags[tag]
            elif self.GROUP_DELIMITER in tag:
                groups[tag_split[0]].append(tag_short_name)

        return groups
