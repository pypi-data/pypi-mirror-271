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
    'GetAwsVpcPeeringConnectionResult',
    'AwaitableGetAwsVpcPeeringConnectionResult',
    'get_aws_vpc_peering_connection',
    'get_aws_vpc_peering_connection_output',
]

@pulumi.output_type
class GetAwsVpcPeeringConnectionResult:
    """
    A collection of values returned by getAwsVpcPeeringConnection.
    """
    def __init__(__self__, aws_account_id=None, aws_vpc_id=None, aws_vpc_peering_connection_id=None, aws_vpc_region=None, id=None, state=None, state_info=None, vpc_id=None):
        if aws_account_id and not isinstance(aws_account_id, str):
            raise TypeError("Expected argument 'aws_account_id' to be a str")
        pulumi.set(__self__, "aws_account_id", aws_account_id)
        if aws_vpc_id and not isinstance(aws_vpc_id, str):
            raise TypeError("Expected argument 'aws_vpc_id' to be a str")
        pulumi.set(__self__, "aws_vpc_id", aws_vpc_id)
        if aws_vpc_peering_connection_id and not isinstance(aws_vpc_peering_connection_id, str):
            raise TypeError("Expected argument 'aws_vpc_peering_connection_id' to be a str")
        pulumi.set(__self__, "aws_vpc_peering_connection_id", aws_vpc_peering_connection_id)
        if aws_vpc_region and not isinstance(aws_vpc_region, str):
            raise TypeError("Expected argument 'aws_vpc_region' to be a str")
        pulumi.set(__self__, "aws_vpc_region", aws_vpc_region)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if state_info and not isinstance(state_info, dict):
            raise TypeError("Expected argument 'state_info' to be a dict")
        pulumi.set(__self__, "state_info", state_info)
        if vpc_id and not isinstance(vpc_id, str):
            raise TypeError("Expected argument 'vpc_id' to be a str")
        pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="awsAccountId")
    def aws_account_id(self) -> str:
        """
        AWS account ID. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "aws_account_id")

    @property
    @pulumi.getter(name="awsVpcId")
    def aws_vpc_id(self) -> str:
        """
        AWS VPC ID. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "aws_vpc_id")

    @property
    @pulumi.getter(name="awsVpcPeeringConnectionId")
    def aws_vpc_peering_connection_id(self) -> str:
        """
        The ID of the AWS VPC peering connection.
        """
        return pulumi.get(self, "aws_vpc_peering_connection_id")

    @property
    @pulumi.getter(name="awsVpcRegion")
    def aws_vpc_region(self) -> str:
        """
        The AWS region of the peered VPC, if different from the Aiven VPC region. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "aws_vpc_region")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        The state of the peering connection.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="stateInfo")
    def state_info(self) -> Mapping[str, Any]:
        """
        State-specific help or error information.
        """
        return pulumi.get(self, "state_info")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> str:
        """
        The ID of the Aiven VPC. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "vpc_id")


class AwaitableGetAwsVpcPeeringConnectionResult(GetAwsVpcPeeringConnectionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAwsVpcPeeringConnectionResult(
            aws_account_id=self.aws_account_id,
            aws_vpc_id=self.aws_vpc_id,
            aws_vpc_peering_connection_id=self.aws_vpc_peering_connection_id,
            aws_vpc_region=self.aws_vpc_region,
            id=self.id,
            state=self.state,
            state_info=self.state_info,
            vpc_id=self.vpc_id)


def get_aws_vpc_peering_connection(aws_account_id: Optional[str] = None,
                                   aws_vpc_id: Optional[str] = None,
                                   aws_vpc_region: Optional[str] = None,
                                   vpc_id: Optional[str] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAwsVpcPeeringConnectionResult:
    """
    Gets information about an AWS VPC peering connection.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aiven as aiven

    example_vpc = aiven.ProjectVpc("example_vpc",
        project=example_project["project"],
        cloud_name="google-europe-west1",
        network_cidr="192.168.1.0/24")
    aws_to_aiven_peering = example_vpc.id.apply(lambda id: aiven.get_aws_vpc_peering_connection_output(vpc_id=id,
        aws_account_id=aws_id,
        aws_vpc_id="vpc-1a2b3c4d5e6f7g8h9",
        aws_vpc_region="aws-us-east-2"))
    ```


    :param str aws_account_id: AWS account ID. Changing this property forces recreation of the resource.
    :param str aws_vpc_id: AWS VPC ID. Changing this property forces recreation of the resource.
    :param str aws_vpc_region: The AWS region of the peered VPC, if different from the Aiven VPC region. Changing this property forces recreation of the resource.
    :param str vpc_id: The ID of the Aiven VPC. Changing this property forces recreation of the resource.
    """
    __args__ = dict()
    __args__['awsAccountId'] = aws_account_id
    __args__['awsVpcId'] = aws_vpc_id
    __args__['awsVpcRegion'] = aws_vpc_region
    __args__['vpcId'] = vpc_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aiven:index/getAwsVpcPeeringConnection:getAwsVpcPeeringConnection', __args__, opts=opts, typ=GetAwsVpcPeeringConnectionResult).value

    return AwaitableGetAwsVpcPeeringConnectionResult(
        aws_account_id=pulumi.get(__ret__, 'aws_account_id'),
        aws_vpc_id=pulumi.get(__ret__, 'aws_vpc_id'),
        aws_vpc_peering_connection_id=pulumi.get(__ret__, 'aws_vpc_peering_connection_id'),
        aws_vpc_region=pulumi.get(__ret__, 'aws_vpc_region'),
        id=pulumi.get(__ret__, 'id'),
        state=pulumi.get(__ret__, 'state'),
        state_info=pulumi.get(__ret__, 'state_info'),
        vpc_id=pulumi.get(__ret__, 'vpc_id'))


@_utilities.lift_output_func(get_aws_vpc_peering_connection)
def get_aws_vpc_peering_connection_output(aws_account_id: Optional[pulumi.Input[str]] = None,
                                          aws_vpc_id: Optional[pulumi.Input[str]] = None,
                                          aws_vpc_region: Optional[pulumi.Input[str]] = None,
                                          vpc_id: Optional[pulumi.Input[str]] = None,
                                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAwsVpcPeeringConnectionResult]:
    """
    Gets information about an AWS VPC peering connection.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aiven as aiven

    example_vpc = aiven.ProjectVpc("example_vpc",
        project=example_project["project"],
        cloud_name="google-europe-west1",
        network_cidr="192.168.1.0/24")
    aws_to_aiven_peering = example_vpc.id.apply(lambda id: aiven.get_aws_vpc_peering_connection_output(vpc_id=id,
        aws_account_id=aws_id,
        aws_vpc_id="vpc-1a2b3c4d5e6f7g8h9",
        aws_vpc_region="aws-us-east-2"))
    ```


    :param str aws_account_id: AWS account ID. Changing this property forces recreation of the resource.
    :param str aws_vpc_id: AWS VPC ID. Changing this property forces recreation of the resource.
    :param str aws_vpc_region: The AWS region of the peered VPC, if different from the Aiven VPC region. Changing this property forces recreation of the resource.
    :param str vpc_id: The ID of the Aiven VPC. Changing this property forces recreation of the resource.
    """
    ...
