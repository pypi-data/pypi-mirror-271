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
    'GetHttpRetryResult',
]

@pulumi.output_type
class GetHttpRetryResult(dict):
    def __init__(__self__, *,
                 attempts: Optional[int] = None,
                 max_delay_ms: Optional[int] = None,
                 min_delay_ms: Optional[int] = None):
        """
        :param int attempts: The number of times the request is to be retried. For example, if 2 is specified, the request will be tried a maximum of 3 times.
        :param int max_delay_ms: The maximum delay between retry requests in milliseconds.
        :param int min_delay_ms: The minimum delay between retry requests in milliseconds.
        """
        if attempts is not None:
            pulumi.set(__self__, "attempts", attempts)
        if max_delay_ms is not None:
            pulumi.set(__self__, "max_delay_ms", max_delay_ms)
        if min_delay_ms is not None:
            pulumi.set(__self__, "min_delay_ms", min_delay_ms)

    @property
    @pulumi.getter
    def attempts(self) -> Optional[int]:
        """
        The number of times the request is to be retried. For example, if 2 is specified, the request will be tried a maximum of 3 times.
        """
        return pulumi.get(self, "attempts")

    @property
    @pulumi.getter(name="maxDelayMs")
    def max_delay_ms(self) -> Optional[int]:
        """
        The maximum delay between retry requests in milliseconds.
        """
        return pulumi.get(self, "max_delay_ms")

    @property
    @pulumi.getter(name="minDelayMs")
    def min_delay_ms(self) -> Optional[int]:
        """
        The minimum delay between retry requests in milliseconds.
        """
        return pulumi.get(self, "min_delay_ms")


