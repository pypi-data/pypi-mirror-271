from .generic_crud import GenericCRUD
from .constants import UpdateStatus
from datetime import datetime


class SyncConflictResolution(GenericCRUD):
    def __init__(self, default_schema_name: str = None, default_table_name: str = None,
                 default_view_table_name: str = None, default_id_column_name: str = None,
                 default_select_clause_value: str = "updated_timestamp",
                 default_where: str = None):
        GenericCRUD.__init__(self, default_schema_name=default_schema_name, default_table_name=default_table_name,
                             default_view_table_name=default_view_table_name, default_id_column_name=default_id_column_name,
                             default_select_clause_value=default_select_clause_value, default_where=default_where)

    def get_update_status_by_where(self, remote_last_modified_timestamp: str, params: str,
                                   schema_name: str = None, view_table_name: str = None,
                                   where: str = None,  select_clause_value: str = None) -> UpdateStatus:
        """
        Get the status of the update by the where clause
        :param remote_last_modified_timestamp: str
        :param schema_name: str
        :param view_table_name: str
        :param where: str
        :param select_clause: str
        :return: str
        """
        if not schema_name:
            schema_name = self.schema_name
        if not view_table_name:
            view_table_name = self.default_view_table_name
        if not select_clause_value:
            select_clause_value = self.default_select_clause_value
        if not where:
            where = self.default_where
        if not view_table_name or not where or not schema_name:
            self.logger.error("view_table_name, where or schema was not provided")
            return "error"
        local_updated_timestamp = self.select_one_value_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where, params=params)
        remote_last_modified_timestamp: datetime = datetime.strptime(remote_last_modified_timestamp, '%Y-%m-%d %H:%M:%S')
        if local_updated_timestamp is None or remote_last_modified_timestamp > local_updated_timestamp:
            return UpdateStatus.UPDATE_CIRCLEZ
        elif remote_last_modified_timestamp < local_updated_timestamp:
            return UpdateStatus.UPDATE_DATA_SOURCE
        else:
            return UpdateStatus.DONT_UPDATE

    def get_update_status_by_id(self, remote_last_modified_timestamp: str, id_column_value: str,
                                schema_name: str = None, view_table_name: str = None, id_column_name: str = None,
                                select_clause_value: str = None) -> UpdateStatus:
        """
        Get the status of the update by the id
        :param remote_last_modified_timestamp: str
        :param id: str
        :param schema_name: str
        :param view_table_name: str
        :param id_column_name: str
        :param id_column_value: str
        :param select_clause_value: str
        :return: str
        """
        if not schema_name:
            schema_name = self.schema_name
        if not view_table_name:
            view_table_name = self.default_view_table_name
        if not id_column_name:
            id_column_name = self.default_column
        if not select_clause_value:
            select_clause_value = self.default_select_clause_value
        if not view_table_name or not id_column_name or not schema_name:
            self.logger.error("view_table_name, id_column_name or schema was not provided")
            return "error"
        local_updated_timestamp = self.select_one_value_by_id(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            id_column_name=id_column_name, id_column_value=id_column_value)
        remote_last_modified_timestamp: datetime = datetime.strptime(remote_last_modified_timestamp, '%Y-%m-%d %H:%M:%S')
        if local_updated_timestamp is None or remote_last_modified_timestamp > local_updated_timestamp:
            return UpdateStatus.UPDATE_CIRCLEZ
        elif remote_last_modified_timestamp < local_updated_timestamp:
            return UpdateStatus.UPDATE_DATA_SOURCE
        else:
            return UpdateStatus.DONT_UPDATE
