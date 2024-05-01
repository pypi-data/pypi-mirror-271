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
    'GetAccountLoginsResult',
    'AwaitableGetAccountLoginsResult',
    'get_account_logins',
    'get_account_logins_output',
]

@pulumi.output_type
class GetAccountLoginsResult:
    """
    A collection of values returned by getAccountLogins.
    """
    def __init__(__self__, filters=None, id=None, logins=None):
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if logins and not isinstance(logins, list):
            raise TypeError("Expected argument 'logins' to be a list")
        pulumi.set(__self__, "logins", logins)

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetAccountLoginsFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The unique ID of this login object.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def logins(self) -> Optional[Sequence['outputs.GetAccountLoginsLoginResult']]:
        return pulumi.get(self, "logins")


class AwaitableGetAccountLoginsResult(GetAccountLoginsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAccountLoginsResult(
            filters=self.filters,
            id=self.id,
            logins=self.logins)


def get_account_logins(filters: Optional[Sequence[pulumi.InputType['GetAccountLoginsFilterArgs']]] = None,
                       logins: Optional[Sequence[pulumi.InputType['GetAccountLoginsLoginArgs']]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAccountLoginsResult:
    """
    Provides information about Linode account logins that match a set of filters.

    ## Example Usage

    The following example shows how one might use this data source to access information about a Linode account login.

    ```python
    import pulumi
    import pulumi_linode as linode

    filtered_account_logins = linode.get_account_logins(filters=[
        linode.GetAccountLoginsFilterArgs(
            name="restricted",
            values=["true"],
        ),
        linode.GetAccountLoginsFilterArgs(
            name="username",
            values=["myUsername"],
        ),
    ])
    pulumi.export("loginIds", [__item.id for __item in filtered_account_logins.logins])
    ```

    ## Filterable Fields

    * `ip`

    * `restricted`

    * `username`
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['logins'] = logins
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('linode:index/getAccountLogins:getAccountLogins', __args__, opts=opts, typ=GetAccountLoginsResult).value

    return AwaitableGetAccountLoginsResult(
        filters=pulumi.get(__ret__, 'filters'),
        id=pulumi.get(__ret__, 'id'),
        logins=pulumi.get(__ret__, 'logins'))


@_utilities.lift_output_func(get_account_logins)
def get_account_logins_output(filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetAccountLoginsFilterArgs']]]]] = None,
                              logins: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetAccountLoginsLoginArgs']]]]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAccountLoginsResult]:
    """
    Provides information about Linode account logins that match a set of filters.

    ## Example Usage

    The following example shows how one might use this data source to access information about a Linode account login.

    ```python
    import pulumi
    import pulumi_linode as linode

    filtered_account_logins = linode.get_account_logins(filters=[
        linode.GetAccountLoginsFilterArgs(
            name="restricted",
            values=["true"],
        ),
        linode.GetAccountLoginsFilterArgs(
            name="username",
            values=["myUsername"],
        ),
    ])
    pulumi.export("loginIds", [__item.id for __item in filtered_account_logins.logins])
    ```

    ## Filterable Fields

    * `ip`

    * `restricted`

    * `username`
    """
    ...
