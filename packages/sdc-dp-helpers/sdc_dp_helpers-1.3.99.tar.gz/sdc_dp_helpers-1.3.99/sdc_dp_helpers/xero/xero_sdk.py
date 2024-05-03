# pylint: disable=too-few-public-methods, unused-import ,attribute-defined-outside-init,broad-exception-raise,trailing-whitespace,line-too-long,no-member,broad-exception-raised,bare-except,too-many-arguments,arguments-differ,wildcard-import,broad-exception-caught,unused-wildcard-import
import os
import json
import ast
from abc import abstractmethod
import requests
from oauth2 import *
from xero.auth import OAuth2Credentials
from xero.exceptions import XeroForbidden
from xero import Xero
from sdc_dp_helpers.api_utilities.retry_managers import request_handler, retry_handler


class XeroQuotaException(Exception):
    """Class for Xero  Quota Exception"""


class Authenticator:
    """
    Xero authentication and token refresh
    """

    def __init__(self, config, creds_filepath):
        self.creds_path: str = creds_filepath
        self.config: dict = config

    def token_isvalid(self, creds: OAuth2Credentials) -> bool:
        if not isinstance(creds, OAuth2Credentials):
            raise TypeError("creds is not an object of type OAuth2Credentials")

        return creds.get_tenants()[0]["tenantId"] is not None

    def get_auth_token(self) -> OAuth2Credentials:
        """
        Consumes the client id and the previous auth processes refresh token.
        This returns an authentication token that will last 30 minutes
        to make queries the minute it is used. Or it will expire in 60 days of no use.
        The newly generated last refresh token now needs token stored for
        next use.
        PS: we receive and save the auth_token in a local dir supplied by the encapsulating project
        we never interact with s3 from inside of this class
        """
        self.client_id = self.config.get("client_id", None)
        if not self.client_id:
            raise ValueError("No client_id set")
        if (not self.client_id) or (len(self.client_id) != 32):
            raise ValueError("Invalid client_id")

        with open(self.creds_path, "r") as token_file:
            auth_token = ast.literal_eval(token_file.read())

        auth_creds = OAuth2Credentials(
            self.client_id, client_secret="", token=auth_token
        )
        return self.refresh_auth_token(auth_creds)

    def refresh_auth_token(self, auth_creds: OAuth2Credentials) -> OAuth2Credentials:
        cred = {
            "grant_type": "refresh_token",
            "refresh_token": auth_creds.token["refresh_token"],  #
            "client_id": self.config.get("client_id", None),
        }
        response = requests.post(
            "https://identity.xero.com/connect/token", cred, timeout=30
        )
        auth_token = response.json()
        err_message = auth_token.get("error")
        if err_message:
            raise Exception(err_message)
        with open(self.creds_path, "w") as outfile:
            outfile.write(json.dumps(auth_token))

        auth_creds = OAuth2Credentials(
            self.client_id, client_secret="", token=auth_token
        )
        if not self.token_isvalid(auth_creds):
            raise XeroForbidden(
                f"Error while trying to authenticate the refreshed token: {str(auth_creds)}"
            )
        return auth_creds


class RequestHandler:
    """Interface for  API Call method"""

    def __init__(self, config, creds_filepath):
        self.creds_path: str = creds_filepath
        self.config: dict = config
        self.authenticator = Authenticator(
            config=self.config, creds_filepath=self.creds_path
        )

    @abstractmethod
    def make_api_call(self, **kwargs):
        """Make API Call"""
        raise NotImplementedError


class XeroAPICall:
    "Class for making xero API call"

    def __init__(self, creds_path, config):
        self.creds_filepath = creds_path
        self.config = config

    def get_reports(self, report_name):
        results = []
        get_data_methods = {
            "filtered": ReportsByTrackingOption,
            "notfiltered": ReportsNotFiltered,
        }
        for filterby in self.config["reports"][report_name]["filter"]:
            method_ids_caller = get_data_methods[filterby](
                config=self.config, creds_filepath=self.creds_filepath
            )
            data = method_ids_caller.make_api_call(
                report_name, self.config["reports"][report_name]["params"], filterby
            )
            results.append(data)
        return results

    def get_modules(self, module):
        module_ = Modules(config=self.config, creds_filepath=self.creds_filepath)
        results = module_.make_api_call(module)
        return results


class ReportsNotFiltered(RequestHandler):
    "Class for not Filtered reports"
    def make_api_call(self, report_name, request_params, filterby):
        data_set = {}
        auth_token = self.authenticator.get_auth_token()
        trackingcategories = GetTrackingCategories(
            config=self.config, creds_filepath=self.creds_path
        ).make_api_call()
        params = {}
        option_id = None
        for tracking_category in trackingcategories:
            file_name = (
                report_name
                + "_"
                + filterby
                + "_"
                + tracking_category["TrackingCategoryID"]
            )
            params.update(
                {"trackingCategoryID": tracking_category["TrackingCategoryID"]}
            )
            report = get_report(
                auth_token,
                params,
                option_id,
                self.config["tenant_id"],
                report_name,
                request_params,
            )
            result = {
                "endpoint": report_name,
                "tenant_name": self.config["tenant_name"],
                "trackingCategoryId": tracking_category["TrackingCategoryID"],
                "data": [report],
                "date": request_params.get("date", request_params.get("end_date")),
                "filterby": filterby,
            }
            if result and result is not None:
                data_set.update({file_name: result})
        return data_set


class GetTrackingCategories(RequestHandler):
    "class to get Reports filtered by Tracking categories"

    def make_api_call(self):
        auth_token = self.authenticator.get_auth_token()
        auth_token.tenant_id = self.config.get("tenant_id")
        xero_obj = Xero(auth_token)
        trackingcategories = (
            i for i in xero_obj.trackingcategories.all() if i is not None
        )
        return trackingcategories


class ReportsByTrackingOption(RequestHandler):
    "class to get Reports filtered by TrackingOptionID"

    def make_api_call(self, report_name, request_params, filterby):
        data_set = {}
        trackingcategories = GetTrackingCategories(
            config=self.config, creds_filepath=self.creds_path
        ).make_api_call()
        auth_token = self.authenticator.get_auth_token()
        params = {}

        for tracking_category in trackingcategories:
            option_data = []
            for option_id in tracking_category["Options"]:
                file_name = (
                    report_name
                    + "_"
                    + filterby
                    + "_"
                    + tracking_category["TrackingCategoryID"]
                )
                params.update(
                    {"trackingCategoryID": tracking_category["TrackingCategoryID"]}
                )
                params.update({"TrackingOptionID": option_id["TrackingOptionID"]})
                report = get_report(
                    auth_token,
                    params,
                    option_id,
                    self.config["tenant_id"],
                    report_name,
                    request_params,
                )
                option_data.append(report)
            result = {
                "endpoint": report_name,
                "tenant_name": self.config["tenant_name"],
                "trackingCategoryId": tracking_category["TrackingCategoryID"],
                "data": option_data,
                "date": request_params.get("date", request_params.get("end_date")),
                "filterby": filterby,
            }
            if option_data and option_data is not None:
                data_set.update({file_name: result})
        return data_set


class Modules(RequestHandler):
    "class to get Modules"

    @request_handler(
        wait=int(os.environ.get("REQUEST_WAIT_TIME", 0.1)),
        backoff_factor=float(os.environ.get("REQUEST_BACKOFF_FACTOR", 0.01)),
        backoff_method=os.environ.get("REQUEST_BACKOFF_METHOD", 0.01),
    )
    def run_request(self, xero_client, api_object, request):
        """
        Run the API request that consumes a request payload and site url.
        This separates the request with the request handler from the rest of the logic.
        """
        # To Do Handle API Errors
        api_call = getattr(xero_client, api_object)
        # XeroRateLimitExceeded
        return api_call.filter(
            raw=date_filter_helper(request["from_date"], request["to_date"]),
            page=request["page"],
        )

    def make_api_call(self, module):
        auth_token = self.authenticator.get_auth_token()
        auth_token.tenant_id = self.config.get("tenant_id")
        xero = Xero(auth_token)
        data_set = {}
        if module not in [
            "accounts",
        ]:
            raise ValueError(module + " is not supported or does not exist.")
        data_set[module] = []
        prev_response = None
        page = 1
        while True:
            response = self.run_request(
                xero_client=xero,
                api_object=module,
                request={
                    "from_date": self.config.get("start_date"),
                    "to_date": self.config.get("end_date"),
                    "page": page,
                },
            )
            print(response)
            if len(response) < 1:
                print("Request returned empty payload. breaking...")
                break
            if response == prev_response:
                print("Request returned copy of last payload. breaking...")
            data_set[module] += [
                json.loads(
                    json.dumps(response_obj, indent=4, sort_keys=True, default=str)
                )
                for response_obj in response
            ]
            # ensure the token is still fresh
            auth_token = self.authenticator.get_auth_token()
            prev_response = response
            page += 1
        return data_set


############### helper functions



@retry_handler(exceptions=XeroQuotaException, total_tries=5, initial_wait=5)
def get_report(auth_token, params, option_id, tenant_id, report_name, request_params):
    if report_name in ["ProfitAndLoss"]:
        params = {
            "fromDate": request_params["start_date"],
            "toDate": request_params["end_date"],
        }
    if report_name in ["BalanceSheet"]:
        params.update({"date": request_params.get("date")})
        params.update({"timeframe": request_params.get("timeframe")})
        params.update({"periods": request_params.get("periods")})
    headers = {
        "Authorization": "Bearer " + auth_token.token["access_token"],
        "Xero-Tenant-Id": tenant_id,
        "Accept": "application/json",
    }
    try:
        response = requests.get(
            "https://api.xero.com/api.xro/2.0/Reports/" + report_name,
            params=params,
            headers=headers,
            timeout=30,
        )
        report = json.loads(
            response.text.replace("\r", "").replace("\n", "").strip("'<>() ")
        )
        report = format_values(report, tenant_id, option_id=option_id)
    except Exception as err:
        if err.code == 429:
            raise XeroQuotaException(
                f"Xero Quota Reached" f"Status code: {err.code}, Reason: {err.reason}. "
            ) from err
    return report


def format_values(report, tenant_id, option_id=None):
    for row in range(len(report["Reports"][0]["Rows"])):
        period = report["Reports"][0]["Rows"][0]["Cells"]
        try:
            for report_ in report["Reports"][0]["Rows"][row]["Rows"]:
                for idx, cells in enumerate(report_["Cells"]):
                    cells["Attributes"][0].update({"type": report_["Cells"][0]["Value"]})
                    cells["Attributes"][0].update({"period": period[idx]["Value"]})
        except:
            pass
    if option_id:
        report["TrackingOptionID"] = option_id["TrackingOptionID"]
        report["TrackingOptionName"] = option_id["Name"]
    report["tenantId"] = tenant_id
    return report


def date_filter_helper(from_date: str, to_date: str, filter_field: str = None) -> str:
    """
    Custom implementation of date filters borrowed from:
    https://github.com/ClaimerApp/pyxero/blob/master/xero/basemanager.py
    """
    if not from_date:
        raise ValueError("No from_date set")

    # common date_field inside of the accounts and contacts modules is UpdatedDateUTC
    filter_field = "UpdatedDateUTC" if not filter_field else filter_field
    api_filter = filter_field + ">=DateTime(" + ",".join(from_date.split("-")) + ")"
    if to_date:
        api_filter = (
            api_filter
            + "&&"
            + filter_field
            + "<=DateTime("
            + ",".join(to_date.split("-"))
            + ")"
        )
    # end if
    return api_filter
