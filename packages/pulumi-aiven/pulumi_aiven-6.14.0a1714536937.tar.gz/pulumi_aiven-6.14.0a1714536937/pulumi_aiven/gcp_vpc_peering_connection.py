# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['GcpVpcPeeringConnectionArgs', 'GcpVpcPeeringConnection']

@pulumi.input_type
class GcpVpcPeeringConnectionArgs:
    def __init__(__self__, *,
                 gcp_project_id: pulumi.Input[str],
                 peer_vpc: pulumi.Input[str],
                 vpc_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a GcpVpcPeeringConnection resource.
        :param pulumi.Input[str] gcp_project_id: Google Cloud project ID. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] peer_vpc: Google Cloud VPC network name. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] vpc_id: The VPC the peering connection belongs to. Changing this property forces recreation of the resource.
        """
        pulumi.set(__self__, "gcp_project_id", gcp_project_id)
        pulumi.set(__self__, "peer_vpc", peer_vpc)
        pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="gcpProjectId")
    def gcp_project_id(self) -> pulumi.Input[str]:
        """
        Google Cloud project ID. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "gcp_project_id")

    @gcp_project_id.setter
    def gcp_project_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "gcp_project_id", value)

    @property
    @pulumi.getter(name="peerVpc")
    def peer_vpc(self) -> pulumi.Input[str]:
        """
        Google Cloud VPC network name. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "peer_vpc")

    @peer_vpc.setter
    def peer_vpc(self, value: pulumi.Input[str]):
        pulumi.set(self, "peer_vpc", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Input[str]:
        """
        The VPC the peering connection belongs to. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vpc_id", value)


@pulumi.input_type
class _GcpVpcPeeringConnectionState:
    def __init__(__self__, *,
                 gcp_project_id: Optional[pulumi.Input[str]] = None,
                 peer_vpc: Optional[pulumi.Input[str]] = None,
                 self_link: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None,
                 state_info: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering GcpVpcPeeringConnection resources.
        :param pulumi.Input[str] gcp_project_id: Google Cloud project ID. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] peer_vpc: Google Cloud VPC network name. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] self_link: Computed Google Cloud network peering link.
        :param pulumi.Input[str] state: State of the peering connection.
        :param pulumi.Input[Mapping[str, Any]] state_info: State-specific help or error information.
        :param pulumi.Input[str] vpc_id: The VPC the peering connection belongs to. Changing this property forces recreation of the resource.
        """
        if gcp_project_id is not None:
            pulumi.set(__self__, "gcp_project_id", gcp_project_id)
        if peer_vpc is not None:
            pulumi.set(__self__, "peer_vpc", peer_vpc)
        if self_link is not None:
            pulumi.set(__self__, "self_link", self_link)
        if state is not None:
            pulumi.set(__self__, "state", state)
        if state_info is not None:
            pulumi.set(__self__, "state_info", state_info)
        if vpc_id is not None:
            pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="gcpProjectId")
    def gcp_project_id(self) -> Optional[pulumi.Input[str]]:
        """
        Google Cloud project ID. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "gcp_project_id")

    @gcp_project_id.setter
    def gcp_project_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "gcp_project_id", value)

    @property
    @pulumi.getter(name="peerVpc")
    def peer_vpc(self) -> Optional[pulumi.Input[str]]:
        """
        Google Cloud VPC network name. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "peer_vpc")

    @peer_vpc.setter
    def peer_vpc(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "peer_vpc", value)

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> Optional[pulumi.Input[str]]:
        """
        Computed Google Cloud network peering link.
        """
        return pulumi.get(self, "self_link")

    @self_link.setter
    def self_link(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "self_link", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        State of the peering connection.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state", value)

    @property
    @pulumi.getter(name="stateInfo")
    def state_info(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        State-specific help or error information.
        """
        return pulumi.get(self, "state_info")

    @state_info.setter
    def state_info(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "state_info", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[pulumi.Input[str]]:
        """
        The VPC the peering connection belongs to. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_id", value)


class GcpVpcPeeringConnection(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 gcp_project_id: Optional[pulumi.Input[str]] = None,
                 peer_vpc: Optional[pulumi.Input[str]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates and manages a Google Cloud VPC peering connection.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aiven as aiven

        foo = aiven.GcpVpcPeeringConnection("foo",
            vpc_id=vpc["id"],
            gcp_project_id="xxxx",
            peer_vpc="xxxx")
        ```

        ## Import

        ```sh
        $ pulumi import aiven:index/gcpVpcPeeringConnection:GcpVpcPeeringConnection foo project_name/vpc_id/gcp_project_id/peer_vpc
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] gcp_project_id: Google Cloud project ID. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] peer_vpc: Google Cloud VPC network name. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] vpc_id: The VPC the peering connection belongs to. Changing this property forces recreation of the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: GcpVpcPeeringConnectionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates and manages a Google Cloud VPC peering connection.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aiven as aiven

        foo = aiven.GcpVpcPeeringConnection("foo",
            vpc_id=vpc["id"],
            gcp_project_id="xxxx",
            peer_vpc="xxxx")
        ```

        ## Import

        ```sh
        $ pulumi import aiven:index/gcpVpcPeeringConnection:GcpVpcPeeringConnection foo project_name/vpc_id/gcp_project_id/peer_vpc
        ```

        :param str resource_name: The name of the resource.
        :param GcpVpcPeeringConnectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GcpVpcPeeringConnectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 gcp_project_id: Optional[pulumi.Input[str]] = None,
                 peer_vpc: Optional[pulumi.Input[str]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GcpVpcPeeringConnectionArgs.__new__(GcpVpcPeeringConnectionArgs)

            if gcp_project_id is None and not opts.urn:
                raise TypeError("Missing required property 'gcp_project_id'")
            __props__.__dict__["gcp_project_id"] = gcp_project_id
            if peer_vpc is None and not opts.urn:
                raise TypeError("Missing required property 'peer_vpc'")
            __props__.__dict__["peer_vpc"] = peer_vpc
            if vpc_id is None and not opts.urn:
                raise TypeError("Missing required property 'vpc_id'")
            __props__.__dict__["vpc_id"] = vpc_id
            __props__.__dict__["self_link"] = None
            __props__.__dict__["state"] = None
            __props__.__dict__["state_info"] = None
        super(GcpVpcPeeringConnection, __self__).__init__(
            'aiven:index/gcpVpcPeeringConnection:GcpVpcPeeringConnection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            gcp_project_id: Optional[pulumi.Input[str]] = None,
            peer_vpc: Optional[pulumi.Input[str]] = None,
            self_link: Optional[pulumi.Input[str]] = None,
            state: Optional[pulumi.Input[str]] = None,
            state_info: Optional[pulumi.Input[Mapping[str, Any]]] = None,
            vpc_id: Optional[pulumi.Input[str]] = None) -> 'GcpVpcPeeringConnection':
        """
        Get an existing GcpVpcPeeringConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] gcp_project_id: Google Cloud project ID. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] peer_vpc: Google Cloud VPC network name. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] self_link: Computed Google Cloud network peering link.
        :param pulumi.Input[str] state: State of the peering connection.
        :param pulumi.Input[Mapping[str, Any]] state_info: State-specific help or error information.
        :param pulumi.Input[str] vpc_id: The VPC the peering connection belongs to. Changing this property forces recreation of the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _GcpVpcPeeringConnectionState.__new__(_GcpVpcPeeringConnectionState)

        __props__.__dict__["gcp_project_id"] = gcp_project_id
        __props__.__dict__["peer_vpc"] = peer_vpc
        __props__.__dict__["self_link"] = self_link
        __props__.__dict__["state"] = state
        __props__.__dict__["state_info"] = state_info
        __props__.__dict__["vpc_id"] = vpc_id
        return GcpVpcPeeringConnection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="gcpProjectId")
    def gcp_project_id(self) -> pulumi.Output[str]:
        """
        Google Cloud project ID. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "gcp_project_id")

    @property
    @pulumi.getter(name="peerVpc")
    def peer_vpc(self) -> pulumi.Output[str]:
        """
        Google Cloud VPC network name. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "peer_vpc")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> pulumi.Output[str]:
        """
        Computed Google Cloud network peering link.
        """
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        State of the peering connection.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="stateInfo")
    def state_info(self) -> pulumi.Output[Mapping[str, Any]]:
        """
        State-specific help or error information.
        """
        return pulumi.get(self, "state_info")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Output[str]:
        """
        The VPC the peering connection belongs to. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "vpc_id")

