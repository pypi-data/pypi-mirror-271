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
from ._inputs import *

__all__ = ['WaitingRoomRulesArgs', 'WaitingRoomRules']

@pulumi.input_type
class WaitingRoomRulesArgs:
    def __init__(__self__, *,
                 waiting_room_id: pulumi.Input[str],
                 zone_id: pulumi.Input[str],
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input['WaitingRoomRulesRuleArgs']]]] = None):
        """
        The set of arguments for constructing a WaitingRoomRules resource.
        :param pulumi.Input[str] waiting_room_id: The Waiting Room ID the rules should apply to. **Modifying this attribute will force creation of a new resource.**
        :param pulumi.Input[str] zone_id: The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**
        :param pulumi.Input[Sequence[pulumi.Input['WaitingRoomRulesRuleArgs']]] rules: List of rules to apply to the ruleset.
        """
        pulumi.set(__self__, "waiting_room_id", waiting_room_id)
        pulumi.set(__self__, "zone_id", zone_id)
        if rules is not None:
            pulumi.set(__self__, "rules", rules)

    @property
    @pulumi.getter(name="waitingRoomId")
    def waiting_room_id(self) -> pulumi.Input[str]:
        """
        The Waiting Room ID the rules should apply to. **Modifying this attribute will force creation of a new resource.**
        """
        return pulumi.get(self, "waiting_room_id")

    @waiting_room_id.setter
    def waiting_room_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "waiting_room_id", value)

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

    @property
    @pulumi.getter
    def rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['WaitingRoomRulesRuleArgs']]]]:
        """
        List of rules to apply to the ruleset.
        """
        return pulumi.get(self, "rules")

    @rules.setter
    def rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['WaitingRoomRulesRuleArgs']]]]):
        pulumi.set(self, "rules", value)


@pulumi.input_type
class _WaitingRoomRulesState:
    def __init__(__self__, *,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input['WaitingRoomRulesRuleArgs']]]] = None,
                 waiting_room_id: Optional[pulumi.Input[str]] = None,
                 zone_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering WaitingRoomRules resources.
        :param pulumi.Input[Sequence[pulumi.Input['WaitingRoomRulesRuleArgs']]] rules: List of rules to apply to the ruleset.
        :param pulumi.Input[str] waiting_room_id: The Waiting Room ID the rules should apply to. **Modifying this attribute will force creation of a new resource.**
        :param pulumi.Input[str] zone_id: The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**
        """
        if rules is not None:
            pulumi.set(__self__, "rules", rules)
        if waiting_room_id is not None:
            pulumi.set(__self__, "waiting_room_id", waiting_room_id)
        if zone_id is not None:
            pulumi.set(__self__, "zone_id", zone_id)

    @property
    @pulumi.getter
    def rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['WaitingRoomRulesRuleArgs']]]]:
        """
        List of rules to apply to the ruleset.
        """
        return pulumi.get(self, "rules")

    @rules.setter
    def rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['WaitingRoomRulesRuleArgs']]]]):
        pulumi.set(self, "rules", value)

    @property
    @pulumi.getter(name="waitingRoomId")
    def waiting_room_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Waiting Room ID the rules should apply to. **Modifying this attribute will force creation of a new resource.**
        """
        return pulumi.get(self, "waiting_room_id")

    @waiting_room_id.setter
    def waiting_room_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "waiting_room_id", value)

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


class WaitingRoomRules(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['WaitingRoomRulesRuleArgs']]]]] = None,
                 waiting_room_id: Optional[pulumi.Input[str]] = None,
                 zone_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Cloudflare Waiting Room Rules resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_cloudflare as cloudflare

        example = cloudflare.WaitingRoomRules("example",
            zone_id="0da42c8d2132a9ddaf714f9e7c920711",
            waiting_room_id="d41d8cd98f00b204e9800998ecf8427e",
            rules=[
                cloudflare.WaitingRoomRulesRuleArgs(
                    description="bypass ip list",
                    expression="src.ip in {192.0.2.0 192.0.2.1}",
                    action="bypass_waiting_room",
                    status="enabled",
                ),
                cloudflare.WaitingRoomRulesRuleArgs(
                    description="bypass query string",
                    expression="http.request.uri.query contains \\"bypass=true\\"",
                    action="bypass_waiting_room",
                    status="enabled",
                ),
            ])
        ```

        ## Import

        ```sh
        $ pulumi import cloudflare:index/waitingRoomRules:WaitingRoomRules default <zone_id>/<waiting_room_id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['WaitingRoomRulesRuleArgs']]]] rules: List of rules to apply to the ruleset.
        :param pulumi.Input[str] waiting_room_id: The Waiting Room ID the rules should apply to. **Modifying this attribute will force creation of a new resource.**
        :param pulumi.Input[str] zone_id: The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: WaitingRoomRulesArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Cloudflare Waiting Room Rules resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_cloudflare as cloudflare

        example = cloudflare.WaitingRoomRules("example",
            zone_id="0da42c8d2132a9ddaf714f9e7c920711",
            waiting_room_id="d41d8cd98f00b204e9800998ecf8427e",
            rules=[
                cloudflare.WaitingRoomRulesRuleArgs(
                    description="bypass ip list",
                    expression="src.ip in {192.0.2.0 192.0.2.1}",
                    action="bypass_waiting_room",
                    status="enabled",
                ),
                cloudflare.WaitingRoomRulesRuleArgs(
                    description="bypass query string",
                    expression="http.request.uri.query contains \\"bypass=true\\"",
                    action="bypass_waiting_room",
                    status="enabled",
                ),
            ])
        ```

        ## Import

        ```sh
        $ pulumi import cloudflare:index/waitingRoomRules:WaitingRoomRules default <zone_id>/<waiting_room_id>
        ```

        :param str resource_name: The name of the resource.
        :param WaitingRoomRulesArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WaitingRoomRulesArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['WaitingRoomRulesRuleArgs']]]]] = None,
                 waiting_room_id: Optional[pulumi.Input[str]] = None,
                 zone_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = WaitingRoomRulesArgs.__new__(WaitingRoomRulesArgs)

            __props__.__dict__["rules"] = rules
            if waiting_room_id is None and not opts.urn:
                raise TypeError("Missing required property 'waiting_room_id'")
            __props__.__dict__["waiting_room_id"] = waiting_room_id
            if zone_id is None and not opts.urn:
                raise TypeError("Missing required property 'zone_id'")
            __props__.__dict__["zone_id"] = zone_id
        super(WaitingRoomRules, __self__).__init__(
            'cloudflare:index/waitingRoomRules:WaitingRoomRules',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['WaitingRoomRulesRuleArgs']]]]] = None,
            waiting_room_id: Optional[pulumi.Input[str]] = None,
            zone_id: Optional[pulumi.Input[str]] = None) -> 'WaitingRoomRules':
        """
        Get an existing WaitingRoomRules resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['WaitingRoomRulesRuleArgs']]]] rules: List of rules to apply to the ruleset.
        :param pulumi.Input[str] waiting_room_id: The Waiting Room ID the rules should apply to. **Modifying this attribute will force creation of a new resource.**
        :param pulumi.Input[str] zone_id: The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _WaitingRoomRulesState.__new__(_WaitingRoomRulesState)

        __props__.__dict__["rules"] = rules
        __props__.__dict__["waiting_room_id"] = waiting_room_id
        __props__.__dict__["zone_id"] = zone_id
        return WaitingRoomRules(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def rules(self) -> pulumi.Output[Optional[Sequence['outputs.WaitingRoomRulesRule']]]:
        """
        List of rules to apply to the ruleset.
        """
        return pulumi.get(self, "rules")

    @property
    @pulumi.getter(name="waitingRoomId")
    def waiting_room_id(self) -> pulumi.Output[str]:
        """
        The Waiting Room ID the rules should apply to. **Modifying this attribute will force creation of a new resource.**
        """
        return pulumi.get(self, "waiting_room_id")

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> pulumi.Output[str]:
        """
        The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**
        """
        return pulumi.get(self, "zone_id")

