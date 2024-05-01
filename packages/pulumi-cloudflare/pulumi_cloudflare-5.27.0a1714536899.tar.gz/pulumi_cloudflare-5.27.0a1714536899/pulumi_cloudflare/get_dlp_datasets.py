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
    'GetDlpDatasetsResult',
    'AwaitableGetDlpDatasetsResult',
    'get_dlp_datasets',
    'get_dlp_datasets_output',
]

@pulumi.output_type
class GetDlpDatasetsResult:
    """
    A collection of values returned by getDlpDatasets.
    """
    def __init__(__self__, account_id=None, datasets=None, id=None):
        if account_id and not isinstance(account_id, str):
            raise TypeError("Expected argument 'account_id' to be a str")
        pulumi.set(__self__, "account_id", account_id)
        if datasets and not isinstance(datasets, list):
            raise TypeError("Expected argument 'datasets' to be a list")
        pulumi.set(__self__, "datasets", datasets)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> str:
        """
        The account ID to fetch DLP Datasets from.
        """
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter
    def datasets(self) -> Sequence['outputs.GetDlpDatasetsDatasetResult']:
        """
        A list of DLP Datasets.
        """
        return pulumi.get(self, "datasets")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")


class AwaitableGetDlpDatasetsResult(GetDlpDatasetsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDlpDatasetsResult(
            account_id=self.account_id,
            datasets=self.datasets,
            id=self.id)


def get_dlp_datasets(account_id: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDlpDatasetsResult:
    """
    Use this data source to retrieve all DLP datasets for an account.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_cloudflare as cloudflare

    example = cloudflare.get_dlp_datasets(account_id="f037e56e89293a057740de681ac9abbe")
    ```


    :param str account_id: The account ID to fetch DLP Datasets from.
    """
    __args__ = dict()
    __args__['accountId'] = account_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('cloudflare:index/getDlpDatasets:getDlpDatasets', __args__, opts=opts, typ=GetDlpDatasetsResult).value

    return AwaitableGetDlpDatasetsResult(
        account_id=pulumi.get(__ret__, 'account_id'),
        datasets=pulumi.get(__ret__, 'datasets'),
        id=pulumi.get(__ret__, 'id'))


@_utilities.lift_output_func(get_dlp_datasets)
def get_dlp_datasets_output(account_id: Optional[pulumi.Input[str]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDlpDatasetsResult]:
    """
    Use this data source to retrieve all DLP datasets for an account.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_cloudflare as cloudflare

    example = cloudflare.get_dlp_datasets(account_id="f037e56e89293a057740de681ac9abbe")
    ```


    :param str account_id: The account ID to fetch DLP Datasets from.
    """
    ...
