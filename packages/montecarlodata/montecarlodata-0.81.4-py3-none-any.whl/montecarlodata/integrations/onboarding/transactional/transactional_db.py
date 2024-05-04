import click

from montecarlodata.collector.validation import CollectorValidationService
from montecarlodata.config import Config
from montecarlodata.errors import manage_errors
from montecarlodata.integrations.onboarding.base import BaseOnboardingService
from montecarlodata.integrations.onboarding.fields import (
    TRANSACTIONAL_WAREHOUSE_TYPE,
    TRANSACTIONAL_CONNECTION_TYPE,
)


class TransactionalOnboardingService(CollectorValidationService, BaseOnboardingService):
    def __init__(self, config: Config, **kwargs):
        super().__init__(config, **kwargs)

    @manage_errors
    def onboard_transactional_db(self, **kwargs) -> None:
        """
        Onboard a Transactional DB connection by validating and adding a connection.
        """
        kwargs["connection_type"] = TRANSACTIONAL_CONNECTION_TYPE
        kwargs["warehouse_type"] = TRANSACTIONAL_WAREHOUSE_TYPE

        # Finds all v2 validations for this connection and runs each one.
        # If they all pass, return a temp credentials key
        # If the --skip-validations flag has been used, no validations are run and just a temp key is returned
        key = self.test_new_credentials(**kwargs)

        # Add the connection
        if key:
            self.add_connection(key, **kwargs)
        else:
            click.Abort()
