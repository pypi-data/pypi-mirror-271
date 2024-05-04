# pylint: disable=unused-import
"""Validators for DAPI."""

from .activerecord import ActiveRecordDapiValidator
from .base import DapiValidator
from .dbt import DbtDapiValidator
from .pynamodb import PynamodbDapiValidator
from .sqlalchemy import SqlAlchemyDapiValidator

DAPI_INTEGRATIONS_VALIDATORS = {
    "activerecord": ActiveRecordDapiValidator,
    "dbt": DbtDapiValidator,
    # Need to support static parsing for PynamoDB
    "pynamodb": None,
    # Need to support static parsing for SQLAlchemy
    "sqlalchemy": None,
    "sequelize": None,
    "typeorm": None,
}
