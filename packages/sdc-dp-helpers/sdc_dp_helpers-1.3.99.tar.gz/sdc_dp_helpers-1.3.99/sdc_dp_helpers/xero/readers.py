# pylint: disable=no-member,inconsistent-return-statements,wrong-import-order,broad-exception-raised,no-else-return,arguments-differ
from sdc_dp_helpers.api_utilities.file_managers import load_file
from sdc_dp_helpers.xero.xero_sdk import XeroAPICall
from sdc_dp_helpers.base_readers import BaseReader
class XeroReader(BaseReader):
    """
        Xero reader
    """
    def __init__(self,  creds_path: str, config_path: str):
        self.creds_path: str = creds_path
        self.config: dict = load_file(config_path, "yml")
        self.service = self._get_auth()

    def _get_auth(self):
        self.service = XeroAPICall(
            config=self.config, creds_path=self.creds_path)
        return self.service

    def _query_handler(self):
        data={}
        if self.config.get("reports"):
            for report in self.config['reports'].keys():
                data[report] = self.service.get_reports(report)
        if self.config.get("modules"):
            for module in self.config.get("modules", []):
                data[module] = self.service.get_modules(module)
        return data

    def run_query(self):
        payload = self._query_handler()
        if payload:
            self.is_success()
            return payload
        else:
            self.not_success()
            print("No data")
