# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['UrlNormalizationSettingsArgs', 'UrlNormalizationSettings']

@pulumi.input_type
class UrlNormalizationSettingsArgs:
    def __init__(__self__, *,
                 scope: pulumi.Input[str],
                 type: pulumi.Input[str],
                 zone_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a UrlNormalizationSettings resource.
        :param pulumi.Input[str] scope: The scope of the URL normalization.
        :param pulumi.Input[str] type: The type of URL normalization performed by Cloudflare.
        :param pulumi.Input[str] zone_id: The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**
        """
        pulumi.set(__self__, "scope", scope)
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "zone_id", zone_id)

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Input[str]:
        """
        The scope of the URL normalization.
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: pulumi.Input[str]):
        pulumi.set(self, "scope", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        The type of URL normalization performed by Cloudflare.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> pulumi.Input[str]:
        """
        The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**
        """
        return pulumi.get(self, "zone_id")

    @zone_id.setter
    def zone_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "zone_id", value)


@pulumi.input_type
class _UrlNormalizationSettingsState:
    def __init__(__self__, *,
                 scope: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 zone_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering UrlNormalizationSettings resources.
        :param pulumi.Input[str] scope: The scope of the URL normalization.
        :param pulumi.Input[str] type: The type of URL normalization performed by Cloudflare.
        :param pulumi.Input[str] zone_id: The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**
        """
        if scope is not None:
            pulumi.set(__self__, "scope", scope)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if zone_id is not None:
            pulumi.set(__self__, "zone_id", zone_id)

    @property
    @pulumi.getter
    def scope(self) -> Optional[pulumi.Input[str]]:
        """
        The scope of the URL normalization.
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "scope", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of URL normalization performed by Cloudflare.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> Optional[pulumi.Input[str]]:
        """
        The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**
        """
        return pulumi.get(self, "zone_id")

    @zone_id.setter
    def zone_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "zone_id", value)


class UrlNormalizationSettings(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 zone_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a resource to manage URL Normalization Settings.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_cloudflare as cloudflare

        example = cloudflare.UrlNormalizationSettings("example",
            zone_id="0da42c8d2132a9ddaf714f9e7c920711",
            type="cloudflare",
            scope="incoming")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] scope: The scope of the URL normalization.
        :param pulumi.Input[str] type: The type of URL normalization performed by Cloudflare.
        :param pulumi.Input[str] zone_id: The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UrlNormalizationSettingsArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to manage URL Normalization Settings.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_cloudflare as cloudflare

        example = cloudflare.UrlNormalizationSettings("example",
            zone_id="0da42c8d2132a9ddaf714f9e7c920711",
            type="cloudflare",
            scope="incoming")
        ```

        :param str resource_name: The name of the resource.
        :param UrlNormalizationSettingsArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UrlNormalizationSettingsArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 zone_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UrlNormalizationSettingsArgs.__new__(UrlNormalizationSettingsArgs)

            if scope is None and not opts.urn:
                raise TypeError("Missing required property 'scope'")
            __props__.__dict__["scope"] = scope
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
            if zone_id is None and not opts.urn:
                raise TypeError("Missing required property 'zone_id'")
            __props__.__dict__["zone_id"] = zone_id
        super(UrlNormalizationSettings, __self__).__init__(
            'cloudflare:index/urlNormalizationSettings:UrlNormalizationSettings',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            scope: Optional[pulumi.Input[str]] = None,
            type: Optional[pulumi.Input[str]] = None,
            zone_id: Optional[pulumi.Input[str]] = None) -> 'UrlNormalizationSettings':
        """
        Get an existing UrlNormalizationSettings resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] scope: The scope of the URL normalization.
        :param pulumi.Input[str] type: The type of URL normalization performed by Cloudflare.
        :param pulumi.Input[str] zone_id: The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _UrlNormalizationSettingsState.__new__(_UrlNormalizationSettingsState)

        __props__.__dict__["scope"] = scope
        __props__.__dict__["type"] = type
        __props__.__dict__["zone_id"] = zone_id
        return UrlNormalizationSettings(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Output[str]:
        """
        The scope of the URL normalization.
        """
        return pulumi.get(self, "scope")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of URL normalization performed by Cloudflare.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> pulumi.Output[str]:
        """
        The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**
        """
        return pulumi.get(self, "zone_id")

