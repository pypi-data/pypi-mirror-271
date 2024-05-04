#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Control Objective Model """

from typing import Any, Optional

from pydantic import Field, ConfigDict

from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.models.regscale_models.regscale_model import RegScaleModel


class ControlObjective(RegScaleModel):
    """RegScale Control Objective"""

    _module_slug = "controlObjectives"
    _unique_fields = ["securityControlId", "name"]

    id: int = 0
    uuid: Optional[str] = None
    name: str
    description: str
    otherId: str = ""  # API does not return if None
    archived: bool = False
    createdById: str = ""
    lastUpdatedById: str = ""
    securityControlId: int
    createdById: str = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    lastUpdatedById: str = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    dateCreated: str = Field(default_factory=get_current_datetime)
    dateLastUpdated: str = Field(default_factory=get_current_datetime)
    objectiveType: str = "objective"

    @staticmethod
    def _get_additional_endpoints() -> ConfigDict:
        """
        Get additional endpoints for the ControlObjective

        :return: Additional endpoints for the ControlObjective
        :rtype: ConfigDict
        """
        return ConfigDict(
            get_all_by_parent="/api/{model_slug}/getByControl/{intParentID}",
            insert="/api/{model_slug}",
            get_by_catalog="/api/{model_slug}/getByCatalog/{catalogId}",
            get_by_catalogue="/api/{model_slug}/getByCatalogue/{catalogId}",
            # Note: This is identical to get_by_catalog, might be redundant
            get_by_control="/api/{model_slug}/getByControl/{controlId}",
            batch_create="/api/{model_slug}/batchCreate",
        )  # type: ignore

    @classmethod
    def get_by_catalog(cls, catalog_id: int) -> list["ControlObjective"]:
        """
        Get a list of objects by catalog.

        :param int catalog_id: The ID of the catalog
        :return: A list of objects
        :rtype: list["ControlObjective"]
        """
        endpoint = cls.get_endpoint("get_by_catalog").format(catalogId=catalog_id)
        return cls._handle_list_response(cls._api_handler.get(endpoint))

    @classmethod
    def get_by_catalogue(cls, catalog_id: int) -> list["ControlObjective"]:
        """
        Get a list of objects by catalogue.

        :param int catalog_id: The ID of the catalogue
        :return: A list of objects
        :rtype: list["ControlObjective"]
        """

        return cls.get_by_catalog(cls, catalog_id)

    @classmethod
    def get_by_control(cls, control_id: int) -> list["ControlObjective"]:
        """
        Get a list of objects by control.

        :param int control_id: The ID of the control
        :return: A list of objects
        :rtype: list["ControlObjective"]
        """
        endpoint = cls.get_endpoint("get_by_control").format(controlId=control_id)
        return cls._handle_list_response(cls._api_handler.get(endpoint))

    @staticmethod
    def from_dict(obj: Any) -> "ControlObjective":
        """
        Create ControlObjective object from dict

        :param Any obj: Dictionary
        :return: ControlObjective class from provided dict
        :rtype: ControlObjective
        """
        _securityControlId = int(obj.get("securityControlId", 0))
        _id = int(obj.get("id", 0))
        _uuid = str(obj.get("uuid"))
        _name = str(obj.get("name"))
        _description = str(obj.get("description"))
        _otherId = str(obj.get("otherId"))
        _objectiveType = str(obj.get("objectiveType"))
        _archived = False
        return ControlObjective(
            _securityControlId,
            _id,
            _uuid,
            _name,
            _description,
            _otherId,
            _objectiveType,
            _archived,
        )
