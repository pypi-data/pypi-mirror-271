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
    'GetCertificatesResult',
    'AwaitableGetCertificatesResult',
    'get_certificates',
    'get_certificates_output',
]

@pulumi.output_type
class GetCertificatesResult:
    """
    A collection of values returned by getCertificates.
    """
    def __init__(__self__, certificates=None, id=None, with_selector=None):
        if certificates and not isinstance(certificates, list):
            raise TypeError("Expected argument 'certificates' to be a list")
        pulumi.set(__self__, "certificates", certificates)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if with_selector and not isinstance(with_selector, str):
            raise TypeError("Expected argument 'with_selector' to be a str")
        pulumi.set(__self__, "with_selector", with_selector)

    @property
    @pulumi.getter
    def certificates(self) -> Sequence['outputs.GetCertificatesCertificateResult']:
        """
        (list) List of all matching certificates. See `data.hcloud_certificate` for schema.
        """
        return pulumi.get(self, "certificates")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="withSelector")
    def with_selector(self) -> Optional[str]:
        return pulumi.get(self, "with_selector")


class AwaitableGetCertificatesResult(GetCertificatesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCertificatesResult(
            certificates=self.certificates,
            id=self.id,
            with_selector=self.with_selector)


def get_certificates(with_selector: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCertificatesResult:
    """
    Provides details about multiple Hetzner Cloud Certificates.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_hcloud as hcloud

    sample_certificate1 = hcloud.get_certificates(with_selector="key=value")
    ```


    :param str with_selector: [Label selector](https://docs.hetzner.cloud/#overview-label-selector)
    """
    __args__ = dict()
    __args__['withSelector'] = with_selector
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('hcloud:index/getCertificates:getCertificates', __args__, opts=opts, typ=GetCertificatesResult).value

    return AwaitableGetCertificatesResult(
        certificates=pulumi.get(__ret__, 'certificates'),
        id=pulumi.get(__ret__, 'id'),
        with_selector=pulumi.get(__ret__, 'with_selector'))


@_utilities.lift_output_func(get_certificates)
def get_certificates_output(with_selector: Optional[pulumi.Input[Optional[str]]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCertificatesResult]:
    """
    Provides details about multiple Hetzner Cloud Certificates.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_hcloud as hcloud

    sample_certificate1 = hcloud.get_certificates(with_selector="key=value")
    ```


    :param str with_selector: [Label selector](https://docs.hetzner.cloud/#overview-label-selector)
    """
    ...
