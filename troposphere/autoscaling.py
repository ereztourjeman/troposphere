# Copyright (c) 2012-2013, Mark Peek <mark@peek.org>
# All rights reserved.
#
# See LICENSE file for full license.

from . import AWSHelperFn, AWSObject, AWSProperty
from .validators import integer, positive_integer


EC2_INSTANCE_LAUNCH = "autoscaling:EC2_INSTANCE_LAUNCH"
EC2_INSTANCE_LAUNCH_ERROR = "autoscaling:EC2_INSTANCE_LAUNCH_ERROR"
EC2_INSTANCE_TERMINATE = "autoscaling:EC2_INSTANCE_TERMINATE"
EC2_INSTANCE_TERMINATE_ERROR = "autoscaling:EC2_INSTANCE_TERMINATE_ERROR"
TEST_NOTIFICATION = "autoscaling:TEST_NOTIFICATION"


class Tag(AWSHelperFn):
    def __init__(self, key, value, propogate):
        self.data = {
            'Key': key,
            'Value': value,
            'PropagateAtLaunch': propogate,
        }

    def JSONrepr(self):
        return self.data


class NotificationConfiguration(AWSProperty):
    props = {
        'TopicARN': (basestring, True),
        'NotificationTypes': (list, True),
    }


class AutoScalingGroup(AWSObject):
    type = "AWS::AutoScaling::AutoScalingGroup"

    props = {
        'AvailabilityZones': (list, True),
        'Cooldown': (integer, False),
        'DesiredCapacity': (integer, False),
        'HealthCheckGracePeriod': (int, False),
        'HealthCheckType': (basestring, False),
        'LaunchConfigurationName': (basestring, True),
        'LoadBalancerNames': (list, False),
        'MaxSize': (positive_integer, True),
        'MinSize': (positive_integer, True),
        'NotificationConfiguration': (NotificationConfiguration, False),
        'Tags': (list, False),  # Although docs say these are required
        'VPCZoneIdentifier': (list, False),
    }

    def validate(self):
        if 'UpdatePolicy' in self.resource:
            update_policy = self.resource['UpdatePolicy']
            if int(update_policy.MinInstancesInService) >= int(self.MaxSize):
                raise ValueError(
                    "The UpdatePolicy attribute "
                    "MinInstancesInService must be less than the "
                    "autoscaling group's MaxSize")
        return True


class LaunchConfiguration(AWSObject):
    type = "AWS::AutoScaling::LaunchConfiguration"

    props = {
        'AssociatePublicIpAddress': (bool, False),
        'BlockDeviceMappings': (list, False),
        'EbsOptimized': (bool, False),
        'IamInstanceProfile': (basestring, False),
        'ImageId': (basestring, True),
        'InstanceMonitoring': (bool, False),
        'InstanceType': (basestring, True),
        'KernelId': (basestring, False),
        'KeyName': (basestring, False),
        'RamDiskId': (basestring, False),
        'SecurityGroups': (list, False),
        'SpotPrice': (basestring, False),
        'UserData': (basestring, False),
    }


class ScalingPolicy(AWSObject):
    type = "AWS::AutoScaling::ScalingPolicy"

    props = {
        'AdjustmentType': (basestring, True),
        'AutoScalingGroupName': (basestring, True),
        'Cooldown': (integer, False),
        'ScalingAdjustment': (basestring, True),
    }


class Trigger(AWSObject):
    type = "AWS::AutoScaling::Trigger"

    props = {
        'AutoScalingGroupName': (basestring, True),
        'BreachDuration': (integer, True),
        'Dimensions': (list, True),
        'LowerBreachScaleIncrement': (integer, False),
        'LowerThreshold': (integer, True),
        'MetricName': (basestring, True),
        'Namespace': (basestring, True),
        'Period': (integer, True),
        'Statistic': (basestring, True),
        'Unit': (basestring, False),
        'UpperBreachScaleIncrement': (integer, False),
        'UpperThreshold': (integer, True),
    }


class EBSBlockDevice(AWSProperty):
    props = {
        'SnapshotId': (basestring, False),
        'VolumeSize': (integer, False),
    }


class BlockDeviceMapping(AWSProperty):
    props = {
        'DeviceName': (basestring, True),
        'Ebs': (EBSBlockDevice, False),
        'VirtualName': (basestring, False),
    }
