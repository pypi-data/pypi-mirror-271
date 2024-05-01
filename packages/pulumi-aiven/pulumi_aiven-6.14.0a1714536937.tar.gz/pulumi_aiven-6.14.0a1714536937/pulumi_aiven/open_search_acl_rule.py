# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['OpenSearchAclRuleArgs', 'OpenSearchAclRule']

@pulumi.input_type
class OpenSearchAclRuleArgs:
    def __init__(__self__, *,
                 index: pulumi.Input[str],
                 permission: pulumi.Input[str],
                 project: pulumi.Input[str],
                 service_name: pulumi.Input[str],
                 username: pulumi.Input[str]):
        """
        The set of arguments for constructing a OpenSearchAclRule resource.
        :param pulumi.Input[str] index: The index pattern for this ACL entry. Maximum length: `249`. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] permission: The permissions for this ACL entry. The possible values are `deny`, `admin`, `read`, `readwrite` and `write`.
        :param pulumi.Input[str] project: Identifies the project this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] service_name: Specifies the name of the service that this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] username: The username for the ACL entry. Maximum length: `40`. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        """
        pulumi.set(__self__, "index", index)
        pulumi.set(__self__, "permission", permission)
        pulumi.set(__self__, "project", project)
        pulumi.set(__self__, "service_name", service_name)
        pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter
    def index(self) -> pulumi.Input[str]:
        """
        The index pattern for this ACL entry. Maximum length: `249`. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "index")

    @index.setter
    def index(self, value: pulumi.Input[str]):
        pulumi.set(self, "index", value)

    @property
    @pulumi.getter
    def permission(self) -> pulumi.Input[str]:
        """
        The permissions for this ACL entry. The possible values are `deny`, `admin`, `read`, `readwrite` and `write`.
        """
        return pulumi.get(self, "permission")

    @permission.setter
    def permission(self, value: pulumi.Input[str]):
        pulumi.set(self, "permission", value)

    @property
    @pulumi.getter
    def project(self) -> pulumi.Input[str]:
        """
        Identifies the project this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: pulumi.Input[str]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> pulumi.Input[str]:
        """
        Specifies the name of the service that this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "service_name")

    @service_name.setter
    def service_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_name", value)

    @property
    @pulumi.getter
    def username(self) -> pulumi.Input[str]:
        """
        The username for the ACL entry. Maximum length: `40`. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: pulumi.Input[str]):
        pulumi.set(self, "username", value)


@pulumi.input_type
class _OpenSearchAclRuleState:
    def __init__(__self__, *,
                 index: Optional[pulumi.Input[str]] = None,
                 permission: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering OpenSearchAclRule resources.
        :param pulumi.Input[str] index: The index pattern for this ACL entry. Maximum length: `249`. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] permission: The permissions for this ACL entry. The possible values are `deny`, `admin`, `read`, `readwrite` and `write`.
        :param pulumi.Input[str] project: Identifies the project this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] service_name: Specifies the name of the service that this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] username: The username for the ACL entry. Maximum length: `40`. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        """
        if index is not None:
            pulumi.set(__self__, "index", index)
        if permission is not None:
            pulumi.set(__self__, "permission", permission)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if service_name is not None:
            pulumi.set(__self__, "service_name", service_name)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter
    def index(self) -> Optional[pulumi.Input[str]]:
        """
        The index pattern for this ACL entry. Maximum length: `249`. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "index")

    @index.setter
    def index(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "index", value)

    @property
    @pulumi.getter
    def permission(self) -> Optional[pulumi.Input[str]]:
        """
        The permissions for this ACL entry. The possible values are `deny`, `admin`, `read`, `readwrite` and `write`.
        """
        return pulumi.get(self, "permission")

    @permission.setter
    def permission(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "permission", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        Identifies the project this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the service that this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "service_name")

    @service_name.setter
    def service_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_name", value)

    @property
    @pulumi.getter
    def username(self) -> Optional[pulumi.Input[str]]:
        """
        The username for the ACL entry. Maximum length: `40`. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username", value)


class OpenSearchAclRule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 index: Optional[pulumi.Input[str]] = None,
                 permission: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The OpenSearch ACL Rule resource models a single ACL Rule for an Aiven OpenSearch service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aiven as aiven

        os_user = aiven.OpensearchUser("os_user",
            project=aiven_project_name,
            service_name=os_test["serviceName"],
            username="documentation-user-1")
        os_user2 = aiven.OpensearchUser("os_user_2",
            project=aiven_project_name,
            service_name=os_test["serviceName"],
            username="documentation-user-2")
        os_acls_config = aiven.OpenSearchAclConfig("os_acls_config",
            project=aiven_project_name,
            service_name=os_test["serviceName"],
            enabled=True,
            extended_acl=False)
        acl_rules = [
            {
                "username": os_user.username,
                "index": "index2",
                "permission": "readwrite",
            },
            {
                "username": os_user.username,
                "index": "index3",
                "permission": "read",
            },
            {
                "username": os_user.username,
                "index": "index5",
                "permission": "deny",
            },
            {
                "username": os_user2.username,
                "index": "index3",
                "permission": "write",
            },
            {
                "username": os_user2.username,
                "index": "index7",
                "permission": "readwrite",
            },
        ]
        os_acl_rule = []
        def create_os_acl_rule(range_body):
            for range in [{"key": k, "value": v} for [k, v] in enumerate(range_body)]:
                os_acl_rule.append(aiven.OpenSearchAclRule(f"os_acl_rule-{range['key']}",
                    project=os_acls_config.project,
                    service_name=os_acls_config.service_name,
                    username=range["value"]["username"],
                    index=range["value"]["index"],
                    permission=range["value"]["permission"]))

        pulumi.Output.all({i: v for i, v in acl_rules}).apply(lambda resolved_outputs: create_os_acl_rule(resolved_outputs[0]))
        ```

        ## Import

        ```sh
        $ pulumi import aiven:index/openSearchAclRule:OpenSearchAclRule os_acl_rule project/service_name/username/index
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] index: The index pattern for this ACL entry. Maximum length: `249`. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] permission: The permissions for this ACL entry. The possible values are `deny`, `admin`, `read`, `readwrite` and `write`.
        :param pulumi.Input[str] project: Identifies the project this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] service_name: Specifies the name of the service that this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] username: The username for the ACL entry. Maximum length: `40`. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: OpenSearchAclRuleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The OpenSearch ACL Rule resource models a single ACL Rule for an Aiven OpenSearch service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aiven as aiven

        os_user = aiven.OpensearchUser("os_user",
            project=aiven_project_name,
            service_name=os_test["serviceName"],
            username="documentation-user-1")
        os_user2 = aiven.OpensearchUser("os_user_2",
            project=aiven_project_name,
            service_name=os_test["serviceName"],
            username="documentation-user-2")
        os_acls_config = aiven.OpenSearchAclConfig("os_acls_config",
            project=aiven_project_name,
            service_name=os_test["serviceName"],
            enabled=True,
            extended_acl=False)
        acl_rules = [
            {
                "username": os_user.username,
                "index": "index2",
                "permission": "readwrite",
            },
            {
                "username": os_user.username,
                "index": "index3",
                "permission": "read",
            },
            {
                "username": os_user.username,
                "index": "index5",
                "permission": "deny",
            },
            {
                "username": os_user2.username,
                "index": "index3",
                "permission": "write",
            },
            {
                "username": os_user2.username,
                "index": "index7",
                "permission": "readwrite",
            },
        ]
        os_acl_rule = []
        def create_os_acl_rule(range_body):
            for range in [{"key": k, "value": v} for [k, v] in enumerate(range_body)]:
                os_acl_rule.append(aiven.OpenSearchAclRule(f"os_acl_rule-{range['key']}",
                    project=os_acls_config.project,
                    service_name=os_acls_config.service_name,
                    username=range["value"]["username"],
                    index=range["value"]["index"],
                    permission=range["value"]["permission"]))

        pulumi.Output.all({i: v for i, v in acl_rules}).apply(lambda resolved_outputs: create_os_acl_rule(resolved_outputs[0]))
        ```

        ## Import

        ```sh
        $ pulumi import aiven:index/openSearchAclRule:OpenSearchAclRule os_acl_rule project/service_name/username/index
        ```

        :param str resource_name: The name of the resource.
        :param OpenSearchAclRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(OpenSearchAclRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 index: Optional[pulumi.Input[str]] = None,
                 permission: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = OpenSearchAclRuleArgs.__new__(OpenSearchAclRuleArgs)

            if index is None and not opts.urn:
                raise TypeError("Missing required property 'index'")
            __props__.__dict__["index"] = index
            if permission is None and not opts.urn:
                raise TypeError("Missing required property 'permission'")
            __props__.__dict__["permission"] = permission
            if project is None and not opts.urn:
                raise TypeError("Missing required property 'project'")
            __props__.__dict__["project"] = project
            if service_name is None and not opts.urn:
                raise TypeError("Missing required property 'service_name'")
            __props__.__dict__["service_name"] = service_name
            if username is None and not opts.urn:
                raise TypeError("Missing required property 'username'")
            __props__.__dict__["username"] = username
        super(OpenSearchAclRule, __self__).__init__(
            'aiven:index/openSearchAclRule:OpenSearchAclRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            index: Optional[pulumi.Input[str]] = None,
            permission: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            service_name: Optional[pulumi.Input[str]] = None,
            username: Optional[pulumi.Input[str]] = None) -> 'OpenSearchAclRule':
        """
        Get an existing OpenSearchAclRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] index: The index pattern for this ACL entry. Maximum length: `249`. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] permission: The permissions for this ACL entry. The possible values are `deny`, `admin`, `read`, `readwrite` and `write`.
        :param pulumi.Input[str] project: Identifies the project this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] service_name: Specifies the name of the service that this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] username: The username for the ACL entry. Maximum length: `40`. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _OpenSearchAclRuleState.__new__(_OpenSearchAclRuleState)

        __props__.__dict__["index"] = index
        __props__.__dict__["permission"] = permission
        __props__.__dict__["project"] = project
        __props__.__dict__["service_name"] = service_name
        __props__.__dict__["username"] = username
        return OpenSearchAclRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def index(self) -> pulumi.Output[str]:
        """
        The index pattern for this ACL entry. Maximum length: `249`. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "index")

    @property
    @pulumi.getter
    def permission(self) -> pulumi.Output[str]:
        """
        The permissions for this ACL entry. The possible values are `deny`, `admin`, `read`, `readwrite` and `write`.
        """
        return pulumi.get(self, "permission")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        Identifies the project this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the service that this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "service_name")

    @property
    @pulumi.getter
    def username(self) -> pulumi.Output[str]:
        """
        The username for the ACL entry. Maximum length: `40`. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "username")

