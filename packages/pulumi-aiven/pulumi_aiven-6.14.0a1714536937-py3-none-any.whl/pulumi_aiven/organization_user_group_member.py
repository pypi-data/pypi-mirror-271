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

__all__ = ['OrganizationUserGroupMemberArgs', 'OrganizationUserGroupMember']

@pulumi.input_type
class OrganizationUserGroupMemberArgs:
    def __init__(__self__, *,
                 group_id: pulumi.Input[str],
                 organization_id: pulumi.Input[str],
                 user_id: pulumi.Input[str],
                 timeouts: Optional[pulumi.Input['OrganizationUserGroupMemberTimeoutsArgs']] = None):
        """
        The set of arguments for constructing a OrganizationUserGroupMember resource.
        :param pulumi.Input[str] group_id: The ID of the user group.
        :param pulumi.Input[str] organization_id: The ID of the organization.
        :param pulumi.Input[str] user_id: The ID of the organization user.
        """
        pulumi.set(__self__, "group_id", group_id)
        pulumi.set(__self__, "organization_id", organization_id)
        pulumi.set(__self__, "user_id", user_id)
        if timeouts is not None:
            pulumi.set(__self__, "timeouts", timeouts)

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> pulumi.Input[str]:
        """
        The ID of the user group.
        """
        return pulumi.get(self, "group_id")

    @group_id.setter
    def group_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "group_id", value)

    @property
    @pulumi.getter(name="organizationId")
    def organization_id(self) -> pulumi.Input[str]:
        """
        The ID of the organization.
        """
        return pulumi.get(self, "organization_id")

    @organization_id.setter
    def organization_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "organization_id", value)

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> pulumi.Input[str]:
        """
        The ID of the organization user.
        """
        return pulumi.get(self, "user_id")

    @user_id.setter
    def user_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "user_id", value)

    @property
    @pulumi.getter
    def timeouts(self) -> Optional[pulumi.Input['OrganizationUserGroupMemberTimeoutsArgs']]:
        return pulumi.get(self, "timeouts")

    @timeouts.setter
    def timeouts(self, value: Optional[pulumi.Input['OrganizationUserGroupMemberTimeoutsArgs']]):
        pulumi.set(self, "timeouts", value)


@pulumi.input_type
class _OrganizationUserGroupMemberState:
    def __init__(__self__, *,
                 group_id: Optional[pulumi.Input[str]] = None,
                 last_activity_time: Optional[pulumi.Input[str]] = None,
                 organization_id: Optional[pulumi.Input[str]] = None,
                 timeouts: Optional[pulumi.Input['OrganizationUserGroupMemberTimeoutsArgs']] = None,
                 user_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering OrganizationUserGroupMember resources.
        :param pulumi.Input[str] group_id: The ID of the user group.
        :param pulumi.Input[str] last_activity_time: Last activity time of the user group member.
        :param pulumi.Input[str] organization_id: The ID of the organization.
        :param pulumi.Input[str] user_id: The ID of the organization user.
        """
        if group_id is not None:
            pulumi.set(__self__, "group_id", group_id)
        if last_activity_time is not None:
            pulumi.set(__self__, "last_activity_time", last_activity_time)
        if organization_id is not None:
            pulumi.set(__self__, "organization_id", organization_id)
        if timeouts is not None:
            pulumi.set(__self__, "timeouts", timeouts)
        if user_id is not None:
            pulumi.set(__self__, "user_id", user_id)

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the user group.
        """
        return pulumi.get(self, "group_id")

    @group_id.setter
    def group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "group_id", value)

    @property
    @pulumi.getter(name="lastActivityTime")
    def last_activity_time(self) -> Optional[pulumi.Input[str]]:
        """
        Last activity time of the user group member.
        """
        return pulumi.get(self, "last_activity_time")

    @last_activity_time.setter
    def last_activity_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_activity_time", value)

    @property
    @pulumi.getter(name="organizationId")
    def organization_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the organization.
        """
        return pulumi.get(self, "organization_id")

    @organization_id.setter
    def organization_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "organization_id", value)

    @property
    @pulumi.getter
    def timeouts(self) -> Optional[pulumi.Input['OrganizationUserGroupMemberTimeoutsArgs']]:
        return pulumi.get(self, "timeouts")

    @timeouts.setter
    def timeouts(self, value: Optional[pulumi.Input['OrganizationUserGroupMemberTimeoutsArgs']]):
        pulumi.set(self, "timeouts", value)

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the organization user.
        """
        return pulumi.get(self, "user_id")

    @user_id.setter
    def user_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_id", value)


class OrganizationUserGroupMember(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 organization_id: Optional[pulumi.Input[str]] = None,
                 timeouts: Optional[pulumi.Input[pulumi.InputType['OrganizationUserGroupMemberTimeoutsArgs']]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Adds and manages users in a [user group](https://aiven.io/docs/platform/concepts/projects_accounts_access#groups).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aiven as aiven

        example = aiven.OrganizationUserGroup("example",
            description="Example group of users.",
            organization_id=main["id"],
            name="Example group")
        project_admin = aiven.OrganizationUserGroupMember("project_admin",
            group_id=example.group_id,
            organization_id=main["id"],
            user_id="u123a456b7890c")
        ```

        ## Import

        ```sh
        $ pulumi import aiven:index/organizationUserGroupMember:OrganizationUserGroupMember project_admin ORGANIZATION_ID/USER_GROUP_ID/USER_ID
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] group_id: The ID of the user group.
        :param pulumi.Input[str] organization_id: The ID of the organization.
        :param pulumi.Input[str] user_id: The ID of the organization user.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: OrganizationUserGroupMemberArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Adds and manages users in a [user group](https://aiven.io/docs/platform/concepts/projects_accounts_access#groups).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aiven as aiven

        example = aiven.OrganizationUserGroup("example",
            description="Example group of users.",
            organization_id=main["id"],
            name="Example group")
        project_admin = aiven.OrganizationUserGroupMember("project_admin",
            group_id=example.group_id,
            organization_id=main["id"],
            user_id="u123a456b7890c")
        ```

        ## Import

        ```sh
        $ pulumi import aiven:index/organizationUserGroupMember:OrganizationUserGroupMember project_admin ORGANIZATION_ID/USER_GROUP_ID/USER_ID
        ```

        :param str resource_name: The name of the resource.
        :param OrganizationUserGroupMemberArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(OrganizationUserGroupMemberArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 organization_id: Optional[pulumi.Input[str]] = None,
                 timeouts: Optional[pulumi.Input[pulumi.InputType['OrganizationUserGroupMemberTimeoutsArgs']]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = OrganizationUserGroupMemberArgs.__new__(OrganizationUserGroupMemberArgs)

            if group_id is None and not opts.urn:
                raise TypeError("Missing required property 'group_id'")
            __props__.__dict__["group_id"] = group_id
            if organization_id is None and not opts.urn:
                raise TypeError("Missing required property 'organization_id'")
            __props__.__dict__["organization_id"] = organization_id
            __props__.__dict__["timeouts"] = timeouts
            if user_id is None and not opts.urn:
                raise TypeError("Missing required property 'user_id'")
            __props__.__dict__["user_id"] = user_id
            __props__.__dict__["last_activity_time"] = None
        super(OrganizationUserGroupMember, __self__).__init__(
            'aiven:index/organizationUserGroupMember:OrganizationUserGroupMember',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            group_id: Optional[pulumi.Input[str]] = None,
            last_activity_time: Optional[pulumi.Input[str]] = None,
            organization_id: Optional[pulumi.Input[str]] = None,
            timeouts: Optional[pulumi.Input[pulumi.InputType['OrganizationUserGroupMemberTimeoutsArgs']]] = None,
            user_id: Optional[pulumi.Input[str]] = None) -> 'OrganizationUserGroupMember':
        """
        Get an existing OrganizationUserGroupMember resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] group_id: The ID of the user group.
        :param pulumi.Input[str] last_activity_time: Last activity time of the user group member.
        :param pulumi.Input[str] organization_id: The ID of the organization.
        :param pulumi.Input[str] user_id: The ID of the organization user.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _OrganizationUserGroupMemberState.__new__(_OrganizationUserGroupMemberState)

        __props__.__dict__["group_id"] = group_id
        __props__.__dict__["last_activity_time"] = last_activity_time
        __props__.__dict__["organization_id"] = organization_id
        __props__.__dict__["timeouts"] = timeouts
        __props__.__dict__["user_id"] = user_id
        return OrganizationUserGroupMember(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> pulumi.Output[str]:
        """
        The ID of the user group.
        """
        return pulumi.get(self, "group_id")

    @property
    @pulumi.getter(name="lastActivityTime")
    def last_activity_time(self) -> pulumi.Output[str]:
        """
        Last activity time of the user group member.
        """
        return pulumi.get(self, "last_activity_time")

    @property
    @pulumi.getter(name="organizationId")
    def organization_id(self) -> pulumi.Output[str]:
        """
        The ID of the organization.
        """
        return pulumi.get(self, "organization_id")

    @property
    @pulumi.getter
    def timeouts(self) -> pulumi.Output[Optional['outputs.OrganizationUserGroupMemberTimeouts']]:
        return pulumi.get(self, "timeouts")

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> pulumi.Output[str]:
        """
        The ID of the organization user.
        """
        return pulumi.get(self, "user_id")

