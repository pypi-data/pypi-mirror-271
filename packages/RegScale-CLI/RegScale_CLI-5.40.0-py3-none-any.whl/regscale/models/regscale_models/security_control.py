#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclass for Security Control in the application """

from dataclasses import asdict
from typing import Any, List, Optional

from pydantic import Field

from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.models.regscale_models import RegScaleModel


class SecurityControl(RegScaleModel):
    """Security Control

    :return: A RegScale Security Control instance
    """

    _module_slug = "securitycontrols"
    _unique_fields = ["controlId", "catalogueId"]

    id: Optional[int] = 0
    isPublic: bool = True
    uuid: Optional[str] = None
    controlId: Optional[str] = None
    sortId: Optional[str] = None
    controlType: Optional[str] = None
    references: Optional[str] = None
    relatedControls: Optional[str] = None
    subControls: Optional[str] = None
    enhancements: Optional[str] = None
    family: Optional[str] = None
    mappings: Optional[str] = None
    assessmentPlan: Optional[str] = None
    weight: float
    catalogueId: int
    practiceLevel: Optional[str] = None
    objectives: Optional[List[object]] = None
    tests: Optional[List[object]] = None
    parameters: Optional[List[object]] = None
    archived: bool = False
    createdById: Optional[str] = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    dateCreated: Optional[str] = Field(default_factory=get_current_datetime)
    lastUpdatedById: Optional[str] = Field(default_factory=RegScaleModel._api_handler.get_user_id)
    dateLastUpdated: Optional[str] = Field(default_factory=get_current_datetime)

    def __hash__(self) -> hash:
        """
        Enable object to be hashable

        :return: Hashed SecurityControl
        :rtype: hash
        """
        return hash((self.controlId, self.catalogueId))

    def __getitem__(self, key: Any) -> Any:
        """
        Get attribute from Pipeline

        :param Any key: Key to get value for
        :return: value of provided key
        :rtype: Any
        """
        return getattr(self, key)

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set attribute in Pipeline with provided key

        :param Any key: Key to change to provided value
        :param Any value: New value for provided Key
        :rtype: None
        """
        return setattr(self, key, value)

    def __eq__(self, other: "SecurityControl") -> bool:
        """
        Update items in SecurityControl class

        :param SecurityControl other: SecurityControl Object to compare to
        :return: Whether the two objects are equal
        :rtype: bool
        """
        return self.controlId == other.controlId and self.catalogueId == other.catalogueID

    @staticmethod
    def lookup_control(
        app: Application,
        control_id: int,
    ) -> "SecurityControl":
        """
        Return a Security Control in RegScale via API

        :param Application app: Application Instance
        :param int control_id: ID of the Security Control to look up
        :return: A Security Control from RegScale
        :rtype: SecurityControl
        """
        api = Api()
        control = api.get(url=app.config["domain"] + f"/api/securitycontrols/{control_id}").json()
        return SecurityControl(**control)

    @staticmethod
    def lookup_control_by_name(app: Application, control_name: str, catalog_id: int) -> Optional["SecurityControl"]:
        """
        Lookup a Security Control by name and catalog ID

        :param Application app: Application instance
        :param str control_name: Name of the security control
        :param int catalog_id: Catalog ID for the security control
        :return: A Security Control from RegScale, if found
        :rtype: Optional[SecurityControl]
        """
        api = Api()
        config = api.config
        res = api.get(config["domain"] + f"/api/securitycontrols/findByUniqueId/{control_name}/{catalog_id}")
        return SecurityControl(**res.json()) if res.status_code == 200 else None
