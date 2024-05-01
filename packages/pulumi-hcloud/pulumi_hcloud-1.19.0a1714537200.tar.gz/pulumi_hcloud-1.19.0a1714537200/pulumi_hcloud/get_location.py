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
    'GetLocationResult',
    'AwaitableGetLocationResult',
    'get_location',
    'get_location_output',
]

@pulumi.output_type
class GetLocationResult:
    """
    A collection of values returned by getLocation.
    """
    def __init__(__self__, city=None, country=None, description=None, id=None, latitude=None, longitude=None, name=None, network_zone=None):
        if city and not isinstance(city, str):
            raise TypeError("Expected argument 'city' to be a str")
        pulumi.set(__self__, "city", city)
        if country and not isinstance(country, str):
            raise TypeError("Expected argument 'country' to be a str")
        pulumi.set(__self__, "country", country)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, int):
            raise TypeError("Expected argument 'id' to be a int")
        pulumi.set(__self__, "id", id)
        if latitude and not isinstance(latitude, float):
            raise TypeError("Expected argument 'latitude' to be a float")
        pulumi.set(__self__, "latitude", latitude)
        if longitude and not isinstance(longitude, float):
            raise TypeError("Expected argument 'longitude' to be a float")
        pulumi.set(__self__, "longitude", longitude)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_zone and not isinstance(network_zone, str):
            raise TypeError("Expected argument 'network_zone' to be a str")
        pulumi.set(__self__, "network_zone", network_zone)

    @property
    @pulumi.getter
    def city(self) -> str:
        """
        (string) City of the location.
        """
        return pulumi.get(self, "city")

    @property
    @pulumi.getter
    def country(self) -> str:
        """
        (string) Country of the location.
        """
        return pulumi.get(self, "country")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        (string) Description of the location.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> int:
        """
        (int) Unique ID of the location.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def latitude(self) -> float:
        """
        (float) Latitude of the city.
        """
        return pulumi.get(self, "latitude")

    @property
    @pulumi.getter
    def longitude(self) -> float:
        """
        (float) Longitude of the city.
        """
        return pulumi.get(self, "longitude")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        (string) Name of the location.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkZone")
    def network_zone(self) -> str:
        """
        (string) Network Zone of the location.
        """
        return pulumi.get(self, "network_zone")


class AwaitableGetLocationResult(GetLocationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLocationResult(
            city=self.city,
            country=self.country,
            description=self.description,
            id=self.id,
            latitude=self.latitude,
            longitude=self.longitude,
            name=self.name,
            network_zone=self.network_zone)


def get_location(id: Optional[int] = None,
                 name: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLocationResult:
    """
    Provides details about a specific Hetzner Cloud Location.
    Use this resource to get detailed information about specific location.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_hcloud as hcloud

    l1 = hcloud.get_location(name="fsn1")
    l2 = hcloud.get_location(id=1)
    ```


    :param int id: ID of the location.
    :param str name: Name of the location.
    """
    __args__ = dict()
    __args__['id'] = id
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('hcloud:index/getLocation:getLocation', __args__, opts=opts, typ=GetLocationResult).value

    return AwaitableGetLocationResult(
        city=pulumi.get(__ret__, 'city'),
        country=pulumi.get(__ret__, 'country'),
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        latitude=pulumi.get(__ret__, 'latitude'),
        longitude=pulumi.get(__ret__, 'longitude'),
        name=pulumi.get(__ret__, 'name'),
        network_zone=pulumi.get(__ret__, 'network_zone'))


@_utilities.lift_output_func(get_location)
def get_location_output(id: Optional[pulumi.Input[Optional[int]]] = None,
                        name: Optional[pulumi.Input[Optional[str]]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLocationResult]:
    """
    Provides details about a specific Hetzner Cloud Location.
    Use this resource to get detailed information about specific location.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_hcloud as hcloud

    l1 = hcloud.get_location(name="fsn1")
    l2 = hcloud.get_location(id=1)
    ```


    :param int id: ID of the location.
    :param str name: Name of the location.
    """
    ...
