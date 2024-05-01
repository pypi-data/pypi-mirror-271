# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['AwsVpcPeeringConnectionArgs', 'AwsVpcPeeringConnection']

@pulumi.input_type
class AwsVpcPeeringConnectionArgs:
    def __init__(__self__, *,
                 aws_account_id: pulumi.Input[str],
                 aws_vpc_id: pulumi.Input[str],
                 aws_vpc_region: pulumi.Input[str],
                 vpc_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a AwsVpcPeeringConnection resource.
        :param pulumi.Input[str] aws_account_id: AWS account ID. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] aws_vpc_id: AWS VPC ID. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] aws_vpc_region: The AWS region of the peered VPC, if different from the Aiven VPC region. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] vpc_id: The ID of the Aiven VPC. Changing this property forces recreation of the resource.
        """
        pulumi.set(__self__, "aws_account_id", aws_account_id)
        pulumi.set(__self__, "aws_vpc_id", aws_vpc_id)
        pulumi.set(__self__, "aws_vpc_region", aws_vpc_region)
        pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="awsAccountId")
    def aws_account_id(self) -> pulumi.Input[str]:
        """
        AWS account ID. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "aws_account_id")

    @aws_account_id.setter
    def aws_account_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "aws_account_id", value)

    @property
    @pulumi.getter(name="awsVpcId")
    def aws_vpc_id(self) -> pulumi.Input[str]:
        """
        AWS VPC ID. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "aws_vpc_id")

    @aws_vpc_id.setter
    def aws_vpc_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "aws_vpc_id", value)

    @property
    @pulumi.getter(name="awsVpcRegion")
    def aws_vpc_region(self) -> pulumi.Input[str]:
        """
        The AWS region of the peered VPC, if different from the Aiven VPC region. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "aws_vpc_region")

    @aws_vpc_region.setter
    def aws_vpc_region(self, value: pulumi.Input[str]):
        pulumi.set(self, "aws_vpc_region", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Input[str]:
        """
        The ID of the Aiven VPC. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vpc_id", value)


@pulumi.input_type
class _AwsVpcPeeringConnectionState:
    def __init__(__self__, *,
                 aws_account_id: Optional[pulumi.Input[str]] = None,
                 aws_vpc_id: Optional[pulumi.Input[str]] = None,
                 aws_vpc_peering_connection_id: Optional[pulumi.Input[str]] = None,
                 aws_vpc_region: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None,
                 state_info: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AwsVpcPeeringConnection resources.
        :param pulumi.Input[str] aws_account_id: AWS account ID. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] aws_vpc_id: AWS VPC ID. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] aws_vpc_peering_connection_id: The ID of the AWS VPC peering connection.
        :param pulumi.Input[str] aws_vpc_region: The AWS region of the peered VPC, if different from the Aiven VPC region. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] state: The state of the peering connection.
        :param pulumi.Input[Mapping[str, Any]] state_info: State-specific help or error information.
        :param pulumi.Input[str] vpc_id: The ID of the Aiven VPC. Changing this property forces recreation of the resource.
        """
        if aws_account_id is not None:
            pulumi.set(__self__, "aws_account_id", aws_account_id)
        if aws_vpc_id is not None:
            pulumi.set(__self__, "aws_vpc_id", aws_vpc_id)
        if aws_vpc_peering_connection_id is not None:
            pulumi.set(__self__, "aws_vpc_peering_connection_id", aws_vpc_peering_connection_id)
        if aws_vpc_region is not None:
            pulumi.set(__self__, "aws_vpc_region", aws_vpc_region)
        if state is not None:
            pulumi.set(__self__, "state", state)
        if state_info is not None:
            pulumi.set(__self__, "state_info", state_info)
        if vpc_id is not None:
            pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="awsAccountId")
    def aws_account_id(self) -> Optional[pulumi.Input[str]]:
        """
        AWS account ID. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "aws_account_id")

    @aws_account_id.setter
    def aws_account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "aws_account_id", value)

    @property
    @pulumi.getter(name="awsVpcId")
    def aws_vpc_id(self) -> Optional[pulumi.Input[str]]:
        """
        AWS VPC ID. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "aws_vpc_id")

    @aws_vpc_id.setter
    def aws_vpc_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "aws_vpc_id", value)

    @property
    @pulumi.getter(name="awsVpcPeeringConnectionId")
    def aws_vpc_peering_connection_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the AWS VPC peering connection.
        """
        return pulumi.get(self, "aws_vpc_peering_connection_id")

    @aws_vpc_peering_connection_id.setter
    def aws_vpc_peering_connection_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "aws_vpc_peering_connection_id", value)

    @property
    @pulumi.getter(name="awsVpcRegion")
    def aws_vpc_region(self) -> Optional[pulumi.Input[str]]:
        """
        The AWS region of the peered VPC, if different from the Aiven VPC region. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "aws_vpc_region")

    @aws_vpc_region.setter
    def aws_vpc_region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "aws_vpc_region", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        The state of the peering connection.
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
        The ID of the Aiven VPC. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_id", value)


class AwsVpcPeeringConnection(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 aws_account_id: Optional[pulumi.Input[str]] = None,
                 aws_vpc_id: Optional[pulumi.Input[str]] = None,
                 aws_vpc_region: Optional[pulumi.Input[str]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates and manages an AWS VPC peering connection with an Aiven VPC.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aiven as aiven

        example_vpc = aiven.ProjectVpc("example_vpc",
            project=example_project["project"],
            cloud_name="aws-us-east-2",
            network_cidr="192.168.1.0/24")
        aws_to_aiven_peering = aiven.AwsVpcPeeringConnection("aws_to_aiven_peering",
            vpc_id=example_vpc.id,
            aws_account_id=aws_id,
            aws_vpc_id="vpc-1a2b3c4d5e6f7g8h9",
            aws_vpc_region="aws-us-east-2")
        ```

        ## Import

        ```sh
        $ pulumi import aiven:index/awsVpcPeeringConnection:AwsVpcPeeringConnection aws_to_aiven_peering PROJECT/VPC_ID/AWS_ACCOUNT_ID/AWS_VPC_ID/AWS_VPC_REGION
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] aws_account_id: AWS account ID. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] aws_vpc_id: AWS VPC ID. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] aws_vpc_region: The AWS region of the peered VPC, if different from the Aiven VPC region. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] vpc_id: The ID of the Aiven VPC. Changing this property forces recreation of the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AwsVpcPeeringConnectionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates and manages an AWS VPC peering connection with an Aiven VPC.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aiven as aiven

        example_vpc = aiven.ProjectVpc("example_vpc",
            project=example_project["project"],
            cloud_name="aws-us-east-2",
            network_cidr="192.168.1.0/24")
        aws_to_aiven_peering = aiven.AwsVpcPeeringConnection("aws_to_aiven_peering",
            vpc_id=example_vpc.id,
            aws_account_id=aws_id,
            aws_vpc_id="vpc-1a2b3c4d5e6f7g8h9",
            aws_vpc_region="aws-us-east-2")
        ```

        ## Import

        ```sh
        $ pulumi import aiven:index/awsVpcPeeringConnection:AwsVpcPeeringConnection aws_to_aiven_peering PROJECT/VPC_ID/AWS_ACCOUNT_ID/AWS_VPC_ID/AWS_VPC_REGION
        ```

        :param str resource_name: The name of the resource.
        :param AwsVpcPeeringConnectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AwsVpcPeeringConnectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 aws_account_id: Optional[pulumi.Input[str]] = None,
                 aws_vpc_id: Optional[pulumi.Input[str]] = None,
                 aws_vpc_region: Optional[pulumi.Input[str]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AwsVpcPeeringConnectionArgs.__new__(AwsVpcPeeringConnectionArgs)

            if aws_account_id is None and not opts.urn:
                raise TypeError("Missing required property 'aws_account_id'")
            __props__.__dict__["aws_account_id"] = aws_account_id
            if aws_vpc_id is None and not opts.urn:
                raise TypeError("Missing required property 'aws_vpc_id'")
            __props__.__dict__["aws_vpc_id"] = aws_vpc_id
            if aws_vpc_region is None and not opts.urn:
                raise TypeError("Missing required property 'aws_vpc_region'")
            __props__.__dict__["aws_vpc_region"] = aws_vpc_region
            if vpc_id is None and not opts.urn:
                raise TypeError("Missing required property 'vpc_id'")
            __props__.__dict__["vpc_id"] = vpc_id
            __props__.__dict__["aws_vpc_peering_connection_id"] = None
            __props__.__dict__["state"] = None
            __props__.__dict__["state_info"] = None
        super(AwsVpcPeeringConnection, __self__).__init__(
            'aiven:index/awsVpcPeeringConnection:AwsVpcPeeringConnection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            aws_account_id: Optional[pulumi.Input[str]] = None,
            aws_vpc_id: Optional[pulumi.Input[str]] = None,
            aws_vpc_peering_connection_id: Optional[pulumi.Input[str]] = None,
            aws_vpc_region: Optional[pulumi.Input[str]] = None,
            state: Optional[pulumi.Input[str]] = None,
            state_info: Optional[pulumi.Input[Mapping[str, Any]]] = None,
            vpc_id: Optional[pulumi.Input[str]] = None) -> 'AwsVpcPeeringConnection':
        """
        Get an existing AwsVpcPeeringConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] aws_account_id: AWS account ID. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] aws_vpc_id: AWS VPC ID. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] aws_vpc_peering_connection_id: The ID of the AWS VPC peering connection.
        :param pulumi.Input[str] aws_vpc_region: The AWS region of the peered VPC, if different from the Aiven VPC region. Changing this property forces recreation of the resource.
        :param pulumi.Input[str] state: The state of the peering connection.
        :param pulumi.Input[Mapping[str, Any]] state_info: State-specific help or error information.
        :param pulumi.Input[str] vpc_id: The ID of the Aiven VPC. Changing this property forces recreation of the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AwsVpcPeeringConnectionState.__new__(_AwsVpcPeeringConnectionState)

        __props__.__dict__["aws_account_id"] = aws_account_id
        __props__.__dict__["aws_vpc_id"] = aws_vpc_id
        __props__.__dict__["aws_vpc_peering_connection_id"] = aws_vpc_peering_connection_id
        __props__.__dict__["aws_vpc_region"] = aws_vpc_region
        __props__.__dict__["state"] = state
        __props__.__dict__["state_info"] = state_info
        __props__.__dict__["vpc_id"] = vpc_id
        return AwsVpcPeeringConnection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="awsAccountId")
    def aws_account_id(self) -> pulumi.Output[str]:
        """
        AWS account ID. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "aws_account_id")

    @property
    @pulumi.getter(name="awsVpcId")
    def aws_vpc_id(self) -> pulumi.Output[str]:
        """
        AWS VPC ID. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "aws_vpc_id")

    @property
    @pulumi.getter(name="awsVpcPeeringConnectionId")
    def aws_vpc_peering_connection_id(self) -> pulumi.Output[str]:
        """
        The ID of the AWS VPC peering connection.
        """
        return pulumi.get(self, "aws_vpc_peering_connection_id")

    @property
    @pulumi.getter(name="awsVpcRegion")
    def aws_vpc_region(self) -> pulumi.Output[str]:
        """
        The AWS region of the peered VPC, if different from the Aiven VPC region. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "aws_vpc_region")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The state of the peering connection.
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
        The ID of the Aiven VPC. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "vpc_id")

