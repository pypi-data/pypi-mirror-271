import functools

import py_scibec_openapi_client
from py_scibec.exceptions import SciBecError
from py_scibec_openapi_client.api import (
    access_account_controller_api,
    access_config_controller_api,
    beamline_controller_api,
    dataset_controller_api,
    device_controller_api,
    experiment_account_controller_api,
    experiment_controller_api,
    functional_account_controller_api,
    scan_controller_api,
    scan_data_controller_api,
    session_controller_api,
    user_controller_api,
)
from py_scibec_openapi_client.exceptions import ApiException
from py_scibec_openapi_client.models import AccessAccount, AccessAccountFilter
from py_scibec_openapi_client.models import AccessAccountFilter1 as AccessAccountFilterWhere
from py_scibec_openapi_client.models import AccessAccountPartial, AccessConfig, AccessConfigFilter
from py_scibec_openapi_client.models import AccessConfigFilter1 as AccessConfigFilterWhere
from py_scibec_openapi_client.models import AccessConfigPartial, Beamline, BeamlineFilter
from py_scibec_openapi_client.models import BeamlineFilter1 as BeamlineFilterWhere
from py_scibec_openapi_client.models import BeamlinePartial, Dataset, DatasetFilter
from py_scibec_openapi_client.models import DatasetFilter1 as DatasetFilterWhere
from py_scibec_openapi_client.models import DatasetPartial, Device, DeviceFilter
from py_scibec_openapi_client.models import DeviceFilter1 as DeviceFilterWhere
from py_scibec_openapi_client.models import (
    DevicePartial,
    Experiment,
    ExperimentAccount,
    ExperimentAccountFilter,
    NewBeamline,
    NewExperiment,
    NewScan,
    NewScanData,
    ScanPartial,
    NewDataset,
)
from py_scibec_openapi_client.models import ExperimentAccountFilter1 as ExperimentAccountFilterWhere
from py_scibec_openapi_client.models import ExperimentFilter
from py_scibec_openapi_client.models import ExperimentFilter1 as ExperimentFilterWhere
from py_scibec_openapi_client.models import (
    ExperimentPartial,
    FunctionalAccount,
    FunctionalAccountFilter,
)
from py_scibec_openapi_client.models import FunctionalAccountFilter1 as FunctionalAccountFilterWhere
from py_scibec_openapi_client.models import FunctionalAccountPartial, Scan, ScanData, ScanDataFilter
from py_scibec_openapi_client.models import ScanDataFilter1 as ScanDataFilterWhere
from py_scibec_openapi_client.models import ScanFilter
from py_scibec_openapi_client.models import ScanFilter1 as ScanFilterWhere
from py_scibec_openapi_client.models import ScanPartial, Session, SessionFilter
from py_scibec_openapi_client.models import SessionFilter1 as SessionFilterWhere
from py_scibec_openapi_client.models import SessionPartial, User, UserControllerLoginRequest


def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not args[0].client:
            raise SciBecError("Not logged in.")
        return func(*args, **kwargs)

    return wrapper


class SciBecModelsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.AccessAccount = AccessAccount
        self.AccessConfig = AccessConfig
        self.Beamline = Beamline
        self.Dataset = Dataset
        self.Device = Device
        self.ScanData = ScanData
        self.Experiment = Experiment
        self.ExperimentAccount = ExperimentAccount
        self.FunctionalAccount = FunctionalAccount
        self.Scan = Scan
        self.Session = Session
        self.User = User


class SciBecCore:
    def __init__(self, host: str = "https://bec.development.psi.ch/api/v1") -> None:
        self.client = None
        self.configuration = py_scibec_openapi_client.Configuration(host=host)
        self.models = SciBecModelsMixin()
        self._access_account = None
        self._access_config = None
        self._beamline = None
        self._dataset = None
        self._device = None
        self._experiment = None
        self._experiment_account = None
        self._functional_account = None
        self._scan = None
        self._scan_data = None
        self._session = None
        self._user = None

    @property
    @login_required
    def access_account(self):
        return self._access_account

    @property
    @login_required
    def access_config(self):
        return self._access_config

    @property
    @login_required
    def beamline(self):
        return self._beamline

    @property
    @login_required
    def dataset(self):
        return self._dataset

    @property
    @login_required
    def device(self):
        return self._device

    @property
    @login_required
    def experiment(self):
        return self._experiment

    @property
    @login_required
    def experiment_account(self):
        return self._experiment_account

    @property
    @login_required
    def functional_account(self):
        return self._functional_account

    @property
    @login_required
    def scan(self):
        return self._scan

    @property
    @login_required
    def scan_data(self):
        return self._scan_data

    @property
    @login_required
    def session(self):
        return self._session

    @property
    @login_required
    def user(self):
        return self._user

    def login(self, username: str = None, password: str = None, token: str = None):
        if not token:
            token = self.get_new_token(username=username, password=password)
        self.configuration.access_token = token
        self.client = py_scibec_openapi_client.ApiClient(self.configuration)

        self._init_controller()

    def get_new_token(self, username: str = None, password: str = None) -> str:
        """
        Get a new token from SciBec. Please note that the token is not stored in the SciBecCore object.
        In general, this method should not be used directly. Instead, use the login method.
        """
        if not username or not password:
            raise SciBecError("Username and password must be provided.")
        client = py_scibec_openapi_client.ApiClient(self.configuration)
        login = user_controller_api.UserControllerApi(client)
        try:
            res = login.user_controller_login(
                UserControllerLoginRequest(principal=username, password=password)
            )
            token = res.token
        except ApiException:
            raise SciBecError("Failed to login.")
        return token

    def _init_controller(self):
        self._access_account = access_account_controller_api.AccessAccountControllerApi(self.client)
        self._access_config = access_config_controller_api.AccessConfigControllerApi(self.client)
        self._beamline = beamline_controller_api.BeamlineControllerApi(self.client)
        self._dataset = dataset_controller_api.DatasetControllerApi(self.client)
        self._device = device_controller_api.DeviceControllerApi(self.client)
        self._experiment = experiment_controller_api.ExperimentControllerApi(self.client)
        self._experiment_account = experiment_account_controller_api.ExperimentAccountControllerApi(
            self.client
        )
        self._functional_account = functional_account_controller_api.FunctionalAccountControllerApi(
            self.client
        )
        self._scan = scan_controller_api.ScanControllerApi(self.client)
        self._scan_data = scan_data_controller_api.ScanDataControllerApi(self.client)
        self._session = session_controller_api.SessionControllerApi(self.client)
        self._user = user_controller_api.UserControllerApi(self.client)
