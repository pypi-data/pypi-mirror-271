# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['AccountTeamMemberArgs', 'AccountTeamMember']

@pulumi.input_type
class AccountTeamMemberArgs:
    def __init__(__self__, *,
                 account_id: pulumi.Input[str],
                 team_id: pulumi.Input[str],
                 user_email: pulumi.Input[str]):
        """
        The set of arguments for constructing a AccountTeamMember resource.
        :param pulumi.Input[str] account_id: The unique account id. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] team_id: An account team id. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] user_email: Is a user email address that first will be invited, and after accepting an invitation, he or she becomes a member of a team. Should be lowercase. Changing this property forces recreation of the resource.
        """
        pulumi.set(__self__, "account_id", account_id)
        pulumi.set(__self__, "team_id", team_id)
        pulumi.set(__self__, "user_email", user_email)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> pulumi.Input[str]:
        """
        The unique account id. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_id", value)

    @property
    @pulumi.getter(name="teamId")
    def team_id(self) -> pulumi.Input[str]:
        """
        An account team id. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "team_id")

    @team_id.setter
    def team_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "team_id", value)

    @property
    @pulumi.getter(name="userEmail")
    def user_email(self) -> pulumi.Input[str]:
        """
        Is a user email address that first will be invited, and after accepting an invitation, he or she becomes a member of a team. Should be lowercase. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "user_email")

    @user_email.setter
    def user_email(self, value: pulumi.Input[str]):
        pulumi.set(self, "user_email", value)


@pulumi.input_type
class _AccountTeamMemberState:
    def __init__(__self__, *,
                 accepted: Optional[pulumi.Input[bool]] = None,
                 account_id: Optional[pulumi.Input[str]] = None,
                 create_time: Optional[pulumi.Input[str]] = None,
                 invited_by_user_email: Optional[pulumi.Input[str]] = None,
                 team_id: Optional[pulumi.Input[str]] = None,
                 user_email: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AccountTeamMember resources.
        :param pulumi.Input[bool] accepted: is a boolean flag that determines whether an invitation was accepted or not by the user. `false` value means that the invitation was sent to the user but not yet accepted. `true` means that the user accepted the invitation and now a member of an account team.
        :param pulumi.Input[str] account_id: The unique account id. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] create_time: Time of creation
        :param pulumi.Input[str] invited_by_user_email: The email address that invited this user.
        :param pulumi.Input[str] team_id: An account team id. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] user_email: Is a user email address that first will be invited, and after accepting an invitation, he or she becomes a member of a team. Should be lowercase. Changing this property forces recreation of the resource.
        """
        if accepted is not None:
            pulumi.set(__self__, "accepted", accepted)
        if account_id is not None:
            pulumi.set(__self__, "account_id", account_id)
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if invited_by_user_email is not None:
            pulumi.set(__self__, "invited_by_user_email", invited_by_user_email)
        if team_id is not None:
            pulumi.set(__self__, "team_id", team_id)
        if user_email is not None:
            pulumi.set(__self__, "user_email", user_email)

    @property
    @pulumi.getter
    def accepted(self) -> Optional[pulumi.Input[bool]]:
        """
        is a boolean flag that determines whether an invitation was accepted or not by the user. `false` value means that the invitation was sent to the user but not yet accepted. `true` means that the user accepted the invitation and now a member of an account team.
        """
        return pulumi.get(self, "accepted")

    @accepted.setter
    def accepted(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "accepted", value)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[pulumi.Input[str]]:
        """
        The unique account id. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_id", value)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[pulumi.Input[str]]:
        """
        Time of creation
        """
        return pulumi.get(self, "create_time")

    @create_time.setter
    def create_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_time", value)

    @property
    @pulumi.getter(name="invitedByUserEmail")
    def invited_by_user_email(self) -> Optional[pulumi.Input[str]]:
        """
        The email address that invited this user.
        """
        return pulumi.get(self, "invited_by_user_email")

    @invited_by_user_email.setter
    def invited_by_user_email(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "invited_by_user_email", value)

    @property
    @pulumi.getter(name="teamId")
    def team_id(self) -> Optional[pulumi.Input[str]]:
        """
        An account team id. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "team_id")

    @team_id.setter
    def team_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "team_id", value)

    @property
    @pulumi.getter(name="userEmail")
    def user_email(self) -> Optional[pulumi.Input[str]]:
        """
        Is a user email address that first will be invited, and after accepting an invitation, he or she becomes a member of a team. Should be lowercase. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "user_email")

    @user_email.setter
    def user_email(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_email", value)


class AccountTeamMember(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[str]] = None,
                 team_id: Optional[pulumi.Input[str]] = None,
                 user_email: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Adds a user as a team member.

        During the creation of this resource, an invite is sent to the address specified in `user_email`.
        The user is added to the team after they accept the invite. Deleting `AccountTeamMember`
        deletes the pending invite if not accepted or removes the user from the team if they already accepted the invite.

        > **Teams are becoming groups**
        Groups are an easier way to control access to your organization's projects and
        services for a group of users.
        Migrate your teams to groups.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aiven as aiven

        main = aiven.AccountTeamMember("main",
            account_id=accoun_t__resourc_e__name["accountId"],
            team_id=tea_m__resourc_e__name["teamId"],
            user_email="user+1@example.com")
        ```

        ## Import

        ```sh
        $ pulumi import aiven:index/accountTeamMember:AccountTeamMember foo account_id/team_id/user_email
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_id: The unique account id. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] team_id: An account team id. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] user_email: Is a user email address that first will be invited, and after accepting an invitation, he or she becomes a member of a team. Should be lowercase. Changing this property forces recreation of the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AccountTeamMemberArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Adds a user as a team member.

        During the creation of this resource, an invite is sent to the address specified in `user_email`.
        The user is added to the team after they accept the invite. Deleting `AccountTeamMember`
        deletes the pending invite if not accepted or removes the user from the team if they already accepted the invite.

        > **Teams are becoming groups**
        Groups are an easier way to control access to your organization's projects and
        services for a group of users.
        Migrate your teams to groups.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aiven as aiven

        main = aiven.AccountTeamMember("main",
            account_id=accoun_t__resourc_e__name["accountId"],
            team_id=tea_m__resourc_e__name["teamId"],
            user_email="user+1@example.com")
        ```

        ## Import

        ```sh
        $ pulumi import aiven:index/accountTeamMember:AccountTeamMember foo account_id/team_id/user_email
        ```

        :param str resource_name: The name of the resource.
        :param AccountTeamMemberArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AccountTeamMemberArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[str]] = None,
                 team_id: Optional[pulumi.Input[str]] = None,
                 user_email: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AccountTeamMemberArgs.__new__(AccountTeamMemberArgs)

            if account_id is None and not opts.urn:
                raise TypeError("Missing required property 'account_id'")
            __props__.__dict__["account_id"] = account_id
            if team_id is None and not opts.urn:
                raise TypeError("Missing required property 'team_id'")
            __props__.__dict__["team_id"] = team_id
            if user_email is None and not opts.urn:
                raise TypeError("Missing required property 'user_email'")
            __props__.__dict__["user_email"] = user_email
            __props__.__dict__["accepted"] = None
            __props__.__dict__["create_time"] = None
            __props__.__dict__["invited_by_user_email"] = None
        super(AccountTeamMember, __self__).__init__(
            'aiven:index/accountTeamMember:AccountTeamMember',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            accepted: Optional[pulumi.Input[bool]] = None,
            account_id: Optional[pulumi.Input[str]] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            invited_by_user_email: Optional[pulumi.Input[str]] = None,
            team_id: Optional[pulumi.Input[str]] = None,
            user_email: Optional[pulumi.Input[str]] = None) -> 'AccountTeamMember':
        """
        Get an existing AccountTeamMember resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] accepted: is a boolean flag that determines whether an invitation was accepted or not by the user. `false` value means that the invitation was sent to the user but not yet accepted. `true` means that the user accepted the invitation and now a member of an account team.
        :param pulumi.Input[str] account_id: The unique account id. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] create_time: Time of creation
        :param pulumi.Input[str] invited_by_user_email: The email address that invited this user.
        :param pulumi.Input[str] team_id: An account team id. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] user_email: Is a user email address that first will be invited, and after accepting an invitation, he or she becomes a member of a team. Should be lowercase. Changing this property forces recreation of the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AccountTeamMemberState.__new__(_AccountTeamMemberState)

        __props__.__dict__["accepted"] = accepted
        __props__.__dict__["account_id"] = account_id
        __props__.__dict__["create_time"] = create_time
        __props__.__dict__["invited_by_user_email"] = invited_by_user_email
        __props__.__dict__["team_id"] = team_id
        __props__.__dict__["user_email"] = user_email
        return AccountTeamMember(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def accepted(self) -> pulumi.Output[bool]:
        """
        is a boolean flag that determines whether an invitation was accepted or not by the user. `false` value means that the invitation was sent to the user but not yet accepted. `true` means that the user accepted the invitation and now a member of an account team.
        """
        return pulumi.get(self, "accepted")

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> pulumi.Output[str]:
        """
        The unique account id. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        Time of creation
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="invitedByUserEmail")
    def invited_by_user_email(self) -> pulumi.Output[str]:
        """
        The email address that invited this user.
        """
        return pulumi.get(self, "invited_by_user_email")

    @property
    @pulumi.getter(name="teamId")
    def team_id(self) -> pulumi.Output[str]:
        """
        An account team id. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "team_id")

    @property
    @pulumi.getter(name="userEmail")
    def user_email(self) -> pulumi.Output[str]:
        """
        Is a user email address that first will be invited, and after accepting an invitation, he or she becomes a member of a team. Should be lowercase. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "user_email")

