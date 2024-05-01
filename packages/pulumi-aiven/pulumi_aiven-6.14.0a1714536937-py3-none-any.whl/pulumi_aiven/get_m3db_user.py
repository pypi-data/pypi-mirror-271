# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetM3dbUserResult',
    'AwaitableGetM3dbUserResult',
    'get_m3db_user',
    'get_m3db_user_output',
]

@pulumi.output_type
class GetM3dbUserResult:
    """
    A collection of values returned by getM3dbUser.
    """
    def __init__(__self__, id=None, password=None, project=None, service_name=None, type=None, username=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if password and not isinstance(password, str):
            raise TypeError("Expected argument 'password' to be a str")
        pulumi.set(__self__, "password", password)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
        if service_name and not isinstance(service_name, str):
            raise TypeError("Expected argument 'service_name' to be a str")
        pulumi.set(__self__, "service_name", service_name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if username and not isinstance(username, str):
            raise TypeError("Expected argument 'username' to be a str")
        pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def password(self) -> str:
        """
        The password of the M3DB User.
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter
    def project(self) -> str:
        """
        Identifies the project this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> str:
        """
        Specifies the name of the service that this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "service_name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the user account. Tells whether the user is the primary account or a regular account.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def username(self) -> str:
        """
        The actual name of the M3DB User. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "username")


class AwaitableGetM3dbUserResult(GetM3dbUserResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetM3dbUserResult(
            id=self.id,
            password=self.password,
            project=self.project,
            service_name=self.service_name,
            type=self.type,
            username=self.username)


def get_m3db_user(project: Optional[str] = None,
                  service_name: Optional[str] = None,
                  username: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetM3dbUserResult:
    """
    The M3DB User data source provides information about the existing Aiven M3DB User.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aiven as aiven

    user = aiven.get_m3db_user(service_name="my-service",
        project="my-project",
        username="user1")
    ```


    :param str project: Identifies the project this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
    :param str service_name: Specifies the name of the service that this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
    :param str username: The actual name of the M3DB User. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
    """
    __args__ = dict()
    __args__['project'] = project
    __args__['serviceName'] = service_name
    __args__['username'] = username
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aiven:index/getM3dbUser:getM3dbUser', __args__, opts=opts, typ=GetM3dbUserResult).value

    return AwaitableGetM3dbUserResult(
        id=pulumi.get(__ret__, 'id'),
        password=pulumi.get(__ret__, 'password'),
        project=pulumi.get(__ret__, 'project'),
        service_name=pulumi.get(__ret__, 'service_name'),
        type=pulumi.get(__ret__, 'type'),
        username=pulumi.get(__ret__, 'username'))


@_utilities.lift_output_func(get_m3db_user)
def get_m3db_user_output(project: Optional[pulumi.Input[str]] = None,
                         service_name: Optional[pulumi.Input[str]] = None,
                         username: Optional[pulumi.Input[str]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetM3dbUserResult]:
    """
    The M3DB User data source provides information about the existing Aiven M3DB User.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aiven as aiven

    user = aiven.get_m3db_user(service_name="my-service",
        project="my-project",
        username="user1")
    ```


    :param str project: Identifies the project this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
    :param str service_name: Specifies the name of the service that this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
    :param str username: The actual name of the M3DB User. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
    """
    ...
