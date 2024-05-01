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

__all__ = [
    'GetKafkaTopicResult',
    'AwaitableGetKafkaTopicResult',
    'get_kafka_topic',
    'get_kafka_topic_output',
]

@pulumi.output_type
class GetKafkaTopicResult:
    """
    A collection of values returned by getKafkaTopic.
    """
    def __init__(__self__, configs=None, id=None, partitions=None, project=None, replication=None, service_name=None, tags=None, termination_protection=None, topic_name=None):
        if configs and not isinstance(configs, list):
            raise TypeError("Expected argument 'configs' to be a list")
        pulumi.set(__self__, "configs", configs)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if partitions and not isinstance(partitions, int):
            raise TypeError("Expected argument 'partitions' to be a int")
        pulumi.set(__self__, "partitions", partitions)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
        if replication and not isinstance(replication, int):
            raise TypeError("Expected argument 'replication' to be a int")
        pulumi.set(__self__, "replication", replication)
        if service_name and not isinstance(service_name, str):
            raise TypeError("Expected argument 'service_name' to be a str")
        pulumi.set(__self__, "service_name", service_name)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if termination_protection and not isinstance(termination_protection, bool):
            raise TypeError("Expected argument 'termination_protection' to be a bool")
        pulumi.set(__self__, "termination_protection", termination_protection)
        if topic_name and not isinstance(topic_name, str):
            raise TypeError("Expected argument 'topic_name' to be a str")
        pulumi.set(__self__, "topic_name", topic_name)

    @property
    @pulumi.getter
    def configs(self) -> Sequence['outputs.GetKafkaTopicConfigResult']:
        """
        Kafka topic configuration
        """
        return pulumi.get(self, "configs")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def partitions(self) -> int:
        """
        The number of partitions to create in the topic.
        """
        return pulumi.get(self, "partitions")

    @property
    @pulumi.getter
    def project(self) -> str:
        """
        Identifies the project this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def replication(self) -> int:
        """
        The replication factor for the topic.
        """
        return pulumi.get(self, "replication")

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> str:
        """
        Specifies the name of the service that this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "service_name")

    @property
    @pulumi.getter
    def tags(self) -> Sequence['outputs.GetKafkaTopicTagResult']:
        """
        Kafka Topic tag.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="terminationProtection")
    def termination_protection(self) -> bool:
        return pulumi.get(self, "termination_protection")

    @property
    @pulumi.getter(name="topicName")
    def topic_name(self) -> str:
        """
        The name of the topic. Changing this property forces recreation of the resource.
        """
        return pulumi.get(self, "topic_name")


class AwaitableGetKafkaTopicResult(GetKafkaTopicResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetKafkaTopicResult(
            configs=self.configs,
            id=self.id,
            partitions=self.partitions,
            project=self.project,
            replication=self.replication,
            service_name=self.service_name,
            tags=self.tags,
            termination_protection=self.termination_protection,
            topic_name=self.topic_name)


def get_kafka_topic(project: Optional[str] = None,
                    service_name: Optional[str] = None,
                    topic_name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetKafkaTopicResult:
    """
    The Kafka Topic data source provides information about the existing Aiven Kafka Topic.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aiven as aiven

    mytesttopic = aiven.get_kafka_topic(project=myproject["project"],
        service_name=myservice["serviceName"],
        topic_name="<TOPIC_NAME>")
    ```


    :param str project: Identifies the project this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
    :param str service_name: Specifies the name of the service that this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
    :param str topic_name: The name of the topic. Changing this property forces recreation of the resource.
    """
    __args__ = dict()
    __args__['project'] = project
    __args__['serviceName'] = service_name
    __args__['topicName'] = topic_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aiven:index/getKafkaTopic:getKafkaTopic', __args__, opts=opts, typ=GetKafkaTopicResult).value

    return AwaitableGetKafkaTopicResult(
        configs=pulumi.get(__ret__, 'configs'),
        id=pulumi.get(__ret__, 'id'),
        partitions=pulumi.get(__ret__, 'partitions'),
        project=pulumi.get(__ret__, 'project'),
        replication=pulumi.get(__ret__, 'replication'),
        service_name=pulumi.get(__ret__, 'service_name'),
        tags=pulumi.get(__ret__, 'tags'),
        termination_protection=pulumi.get(__ret__, 'termination_protection'),
        topic_name=pulumi.get(__ret__, 'topic_name'))


@_utilities.lift_output_func(get_kafka_topic)
def get_kafka_topic_output(project: Optional[pulumi.Input[str]] = None,
                           service_name: Optional[pulumi.Input[str]] = None,
                           topic_name: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetKafkaTopicResult]:
    """
    The Kafka Topic data source provides information about the existing Aiven Kafka Topic.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aiven as aiven

    mytesttopic = aiven.get_kafka_topic(project=myproject["project"],
        service_name=myservice["serviceName"],
        topic_name="<TOPIC_NAME>")
    ```


    :param str project: Identifies the project this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
    :param str service_name: Specifies the name of the service that this resource belongs to. To set up proper dependencies please refer to this variable as a reference. Changing this property forces recreation of the resource.
    :param str topic_name: The name of the topic. Changing this property forces recreation of the resource.
    """
    ...
