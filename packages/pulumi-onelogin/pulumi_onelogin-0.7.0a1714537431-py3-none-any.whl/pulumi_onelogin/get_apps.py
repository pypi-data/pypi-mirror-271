# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = [
    'GetAppsResult',
    'AwaitableGetAppsResult',
    'get_apps',
    'get_apps_output',
]

@pulumi.output_type
class GetAppsResult:
    """
    A collection of values returned by getApps.
    """
    def __init__(__self__, allow_assumed_signin=None, auth_method=None, auth_method_description=None, brand_id=None, configuration=None, connector_id=None, created_at=None, description=None, enforcement_point=None, filters=None, icon_url=None, id=None, login_config=None, name=None, notes=None, parameters=None, policy_id=None, provisioning=None, role_ids=None, sso=None, tab_id=None, updated_at=None, visible=None):
        if allow_assumed_signin and not isinstance(allow_assumed_signin, bool):
            raise TypeError("Expected argument 'allow_assumed_signin' to be a bool")
        pulumi.set(__self__, "allow_assumed_signin", allow_assumed_signin)
        if auth_method and not isinstance(auth_method, int):
            raise TypeError("Expected argument 'auth_method' to be a int")
        pulumi.set(__self__, "auth_method", auth_method)
        if auth_method_description and not isinstance(auth_method_description, str):
            raise TypeError("Expected argument 'auth_method_description' to be a str")
        pulumi.set(__self__, "auth_method_description", auth_method_description)
        if brand_id and not isinstance(brand_id, int):
            raise TypeError("Expected argument 'brand_id' to be a int")
        pulumi.set(__self__, "brand_id", brand_id)
        if configuration and not isinstance(configuration, dict):
            raise TypeError("Expected argument 'configuration' to be a dict")
        pulumi.set(__self__, "configuration", configuration)
        if connector_id and not isinstance(connector_id, int):
            raise TypeError("Expected argument 'connector_id' to be a int")
        pulumi.set(__self__, "connector_id", connector_id)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if enforcement_point and not isinstance(enforcement_point, dict):
            raise TypeError("Expected argument 'enforcement_point' to be a dict")
        pulumi.set(__self__, "enforcement_point", enforcement_point)
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if icon_url and not isinstance(icon_url, str):
            raise TypeError("Expected argument 'icon_url' to be a str")
        pulumi.set(__self__, "icon_url", icon_url)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if login_config and not isinstance(login_config, int):
            raise TypeError("Expected argument 'login_config' to be a int")
        pulumi.set(__self__, "login_config", login_config)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if notes and not isinstance(notes, str):
            raise TypeError("Expected argument 'notes' to be a str")
        pulumi.set(__self__, "notes", notes)
        if parameters and not isinstance(parameters, dict):
            raise TypeError("Expected argument 'parameters' to be a dict")
        pulumi.set(__self__, "parameters", parameters)
        if policy_id and not isinstance(policy_id, int):
            raise TypeError("Expected argument 'policy_id' to be a int")
        pulumi.set(__self__, "policy_id", policy_id)
        if provisioning and not isinstance(provisioning, dict):
            raise TypeError("Expected argument 'provisioning' to be a dict")
        pulumi.set(__self__, "provisioning", provisioning)
        if role_ids and not isinstance(role_ids, list):
            raise TypeError("Expected argument 'role_ids' to be a list")
        pulumi.set(__self__, "role_ids", role_ids)
        if sso and not isinstance(sso, dict):
            raise TypeError("Expected argument 'sso' to be a dict")
        pulumi.set(__self__, "sso", sso)
        if tab_id and not isinstance(tab_id, int):
            raise TypeError("Expected argument 'tab_id' to be a int")
        pulumi.set(__self__, "tab_id", tab_id)
        if updated_at and not isinstance(updated_at, str):
            raise TypeError("Expected argument 'updated_at' to be a str")
        pulumi.set(__self__, "updated_at", updated_at)
        if visible and not isinstance(visible, bool):
            raise TypeError("Expected argument 'visible' to be a bool")
        pulumi.set(__self__, "visible", visible)

    @property
    @pulumi.getter(name="allowAssumedSignin")
    def allow_assumed_signin(self) -> bool:
        return pulumi.get(self, "allow_assumed_signin")

    @property
    @pulumi.getter(name="authMethod")
    def auth_method(self) -> int:
        return pulumi.get(self, "auth_method")

    @property
    @pulumi.getter(name="authMethodDescription")
    def auth_method_description(self) -> str:
        return pulumi.get(self, "auth_method_description")

    @property
    @pulumi.getter(name="brandId")
    def brand_id(self) -> int:
        return pulumi.get(self, "brand_id")

    @property
    @pulumi.getter
    def configuration(self) -> 'outputs.GetAppsConfigurationResult':
        return pulumi.get(self, "configuration")

    @property
    @pulumi.getter(name="connectorId")
    def connector_id(self) -> int:
        return pulumi.get(self, "connector_id")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def description(self) -> str:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="enforcementPoint")
    def enforcement_point(self) -> 'outputs.GetAppsEnforcementPointResult':
        return pulumi.get(self, "enforcement_point")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetAppsFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter(name="iconUrl")
    def icon_url(self) -> str:
        return pulumi.get(self, "icon_url")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="loginConfig")
    def login_config(self) -> int:
        return pulumi.get(self, "login_config")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def notes(self) -> str:
        return pulumi.get(self, "notes")

    @property
    @pulumi.getter
    def parameters(self) -> 'outputs.GetAppsParametersResult':
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="policyId")
    def policy_id(self) -> int:
        return pulumi.get(self, "policy_id")

    @property
    @pulumi.getter
    def provisioning(self) -> 'outputs.GetAppsProvisioningResult':
        return pulumi.get(self, "provisioning")

    @property
    @pulumi.getter(name="roleIds")
    def role_ids(self) -> Sequence[int]:
        return pulumi.get(self, "role_ids")

    @property
    @pulumi.getter
    def sso(self) -> 'outputs.GetAppsSsoResult':
        return pulumi.get(self, "sso")

    @property
    @pulumi.getter(name="tabId")
    def tab_id(self) -> int:
        return pulumi.get(self, "tab_id")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> str:
        return pulumi.get(self, "updated_at")

    @property
    @pulumi.getter
    def visible(self) -> bool:
        return pulumi.get(self, "visible")


class AwaitableGetAppsResult(GetAppsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAppsResult(
            allow_assumed_signin=self.allow_assumed_signin,
            auth_method=self.auth_method,
            auth_method_description=self.auth_method_description,
            brand_id=self.brand_id,
            configuration=self.configuration,
            connector_id=self.connector_id,
            created_at=self.created_at,
            description=self.description,
            enforcement_point=self.enforcement_point,
            filters=self.filters,
            icon_url=self.icon_url,
            id=self.id,
            login_config=self.login_config,
            name=self.name,
            notes=self.notes,
            parameters=self.parameters,
            policy_id=self.policy_id,
            provisioning=self.provisioning,
            role_ids=self.role_ids,
            sso=self.sso,
            tab_id=self.tab_id,
            updated_at=self.updated_at,
            visible=self.visible)


def get_apps(allow_assumed_signin: Optional[bool] = None,
             auth_method: Optional[int] = None,
             auth_method_description: Optional[str] = None,
             brand_id: Optional[int] = None,
             configuration: Optional[pulumi.InputType['GetAppsConfigurationArgs']] = None,
             connector_id: Optional[int] = None,
             created_at: Optional[str] = None,
             description: Optional[str] = None,
             enforcement_point: Optional[pulumi.InputType['GetAppsEnforcementPointArgs']] = None,
             filters: Optional[Sequence[pulumi.InputType['GetAppsFilterArgs']]] = None,
             icon_url: Optional[str] = None,
             login_config: Optional[int] = None,
             name: Optional[str] = None,
             notes: Optional[str] = None,
             parameters: Optional[pulumi.InputType['GetAppsParametersArgs']] = None,
             policy_id: Optional[int] = None,
             provisioning: Optional[pulumi.InputType['GetAppsProvisioningArgs']] = None,
             role_ids: Optional[Sequence[int]] = None,
             sso: Optional[pulumi.InputType['GetAppsSsoArgs']] = None,
             tab_id: Optional[int] = None,
             updated_at: Optional[str] = None,
             visible: Optional[bool] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAppsResult:
    """
    Use this data source to access information about an existing resource.
    """
    __args__ = dict()
    __args__['allowAssumedSignin'] = allow_assumed_signin
    __args__['authMethod'] = auth_method
    __args__['authMethodDescription'] = auth_method_description
    __args__['brandId'] = brand_id
    __args__['configuration'] = configuration
    __args__['connectorId'] = connector_id
    __args__['createdAt'] = created_at
    __args__['description'] = description
    __args__['enforcementPoint'] = enforcement_point
    __args__['filters'] = filters
    __args__['iconUrl'] = icon_url
    __args__['loginConfig'] = login_config
    __args__['name'] = name
    __args__['notes'] = notes
    __args__['parameters'] = parameters
    __args__['policyId'] = policy_id
    __args__['provisioning'] = provisioning
    __args__['roleIds'] = role_ids
    __args__['sso'] = sso
    __args__['tabId'] = tab_id
    __args__['updatedAt'] = updated_at
    __args__['visible'] = visible
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('onelogin:index/getApps:getApps', __args__, opts=opts, typ=GetAppsResult).value

    return AwaitableGetAppsResult(
        allow_assumed_signin=pulumi.get(__ret__, 'allow_assumed_signin'),
        auth_method=pulumi.get(__ret__, 'auth_method'),
        auth_method_description=pulumi.get(__ret__, 'auth_method_description'),
        brand_id=pulumi.get(__ret__, 'brand_id'),
        configuration=pulumi.get(__ret__, 'configuration'),
        connector_id=pulumi.get(__ret__, 'connector_id'),
        created_at=pulumi.get(__ret__, 'created_at'),
        description=pulumi.get(__ret__, 'description'),
        enforcement_point=pulumi.get(__ret__, 'enforcement_point'),
        filters=pulumi.get(__ret__, 'filters'),
        icon_url=pulumi.get(__ret__, 'icon_url'),
        id=pulumi.get(__ret__, 'id'),
        login_config=pulumi.get(__ret__, 'login_config'),
        name=pulumi.get(__ret__, 'name'),
        notes=pulumi.get(__ret__, 'notes'),
        parameters=pulumi.get(__ret__, 'parameters'),
        policy_id=pulumi.get(__ret__, 'policy_id'),
        provisioning=pulumi.get(__ret__, 'provisioning'),
        role_ids=pulumi.get(__ret__, 'role_ids'),
        sso=pulumi.get(__ret__, 'sso'),
        tab_id=pulumi.get(__ret__, 'tab_id'),
        updated_at=pulumi.get(__ret__, 'updated_at'),
        visible=pulumi.get(__ret__, 'visible'))


@_utilities.lift_output_func(get_apps)
def get_apps_output(allow_assumed_signin: Optional[pulumi.Input[Optional[bool]]] = None,
                    auth_method: Optional[pulumi.Input[Optional[int]]] = None,
                    auth_method_description: Optional[pulumi.Input[Optional[str]]] = None,
                    brand_id: Optional[pulumi.Input[Optional[int]]] = None,
                    configuration: Optional[pulumi.Input[Optional[pulumi.InputType['GetAppsConfigurationArgs']]]] = None,
                    connector_id: Optional[pulumi.Input[Optional[int]]] = None,
                    created_at: Optional[pulumi.Input[Optional[str]]] = None,
                    description: Optional[pulumi.Input[Optional[str]]] = None,
                    enforcement_point: Optional[pulumi.Input[Optional[pulumi.InputType['GetAppsEnforcementPointArgs']]]] = None,
                    filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetAppsFilterArgs']]]]] = None,
                    icon_url: Optional[pulumi.Input[Optional[str]]] = None,
                    login_config: Optional[pulumi.Input[Optional[int]]] = None,
                    name: Optional[pulumi.Input[Optional[str]]] = None,
                    notes: Optional[pulumi.Input[Optional[str]]] = None,
                    parameters: Optional[pulumi.Input[Optional[pulumi.InputType['GetAppsParametersArgs']]]] = None,
                    policy_id: Optional[pulumi.Input[Optional[int]]] = None,
                    provisioning: Optional[pulumi.Input[Optional[pulumi.InputType['GetAppsProvisioningArgs']]]] = None,
                    role_ids: Optional[pulumi.Input[Optional[Sequence[int]]]] = None,
                    sso: Optional[pulumi.Input[Optional[pulumi.InputType['GetAppsSsoArgs']]]] = None,
                    tab_id: Optional[pulumi.Input[Optional[int]]] = None,
                    updated_at: Optional[pulumi.Input[Optional[str]]] = None,
                    visible: Optional[pulumi.Input[Optional[bool]]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAppsResult]:
    """
    Use this data source to access information about an existing resource.
    """
    ...
