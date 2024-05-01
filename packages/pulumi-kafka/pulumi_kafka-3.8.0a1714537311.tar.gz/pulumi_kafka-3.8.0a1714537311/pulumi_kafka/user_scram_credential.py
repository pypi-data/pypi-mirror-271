# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['UserScramCredentialArgs', 'UserScramCredential']

@pulumi.input_type
class UserScramCredentialArgs:
    def __init__(__self__, *,
                 password: pulumi.Input[str],
                 scram_mechanism: pulumi.Input[str],
                 username: pulumi.Input[str],
                 scram_iterations: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a UserScramCredential resource.
        :param pulumi.Input[str] password: The password of the credential
        :param pulumi.Input[str] scram_mechanism: The SCRAM mechanism used to generate the credential (SCRAM-SHA-256, SCRAM-SHA-512)
        :param pulumi.Input[str] username: The name of the credential
        :param pulumi.Input[int] scram_iterations: The number of SCRAM iterations used when generating the credential
        """
        pulumi.set(__self__, "password", password)
        pulumi.set(__self__, "scram_mechanism", scram_mechanism)
        pulumi.set(__self__, "username", username)
        if scram_iterations is not None:
            pulumi.set(__self__, "scram_iterations", scram_iterations)

    @property
    @pulumi.getter
    def password(self) -> pulumi.Input[str]:
        """
        The password of the credential
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: pulumi.Input[str]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter(name="scramMechanism")
    def scram_mechanism(self) -> pulumi.Input[str]:
        """
        The SCRAM mechanism used to generate the credential (SCRAM-SHA-256, SCRAM-SHA-512)
        """
        return pulumi.get(self, "scram_mechanism")

    @scram_mechanism.setter
    def scram_mechanism(self, value: pulumi.Input[str]):
        pulumi.set(self, "scram_mechanism", value)

    @property
    @pulumi.getter
    def username(self) -> pulumi.Input[str]:
        """
        The name of the credential
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: pulumi.Input[str]):
        pulumi.set(self, "username", value)

    @property
    @pulumi.getter(name="scramIterations")
    def scram_iterations(self) -> Optional[pulumi.Input[int]]:
        """
        The number of SCRAM iterations used when generating the credential
        """
        return pulumi.get(self, "scram_iterations")

    @scram_iterations.setter
    def scram_iterations(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "scram_iterations", value)


@pulumi.input_type
class _UserScramCredentialState:
    def __init__(__self__, *,
                 password: Optional[pulumi.Input[str]] = None,
                 scram_iterations: Optional[pulumi.Input[int]] = None,
                 scram_mechanism: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering UserScramCredential resources.
        :param pulumi.Input[str] password: The password of the credential
        :param pulumi.Input[int] scram_iterations: The number of SCRAM iterations used when generating the credential
        :param pulumi.Input[str] scram_mechanism: The SCRAM mechanism used to generate the credential (SCRAM-SHA-256, SCRAM-SHA-512)
        :param pulumi.Input[str] username: The name of the credential
        """
        if password is not None:
            pulumi.set(__self__, "password", password)
        if scram_iterations is not None:
            pulumi.set(__self__, "scram_iterations", scram_iterations)
        if scram_mechanism is not None:
            pulumi.set(__self__, "scram_mechanism", scram_mechanism)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The password of the credential
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter(name="scramIterations")
    def scram_iterations(self) -> Optional[pulumi.Input[int]]:
        """
        The number of SCRAM iterations used when generating the credential
        """
        return pulumi.get(self, "scram_iterations")

    @scram_iterations.setter
    def scram_iterations(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "scram_iterations", value)

    @property
    @pulumi.getter(name="scramMechanism")
    def scram_mechanism(self) -> Optional[pulumi.Input[str]]:
        """
        The SCRAM mechanism used to generate the credential (SCRAM-SHA-256, SCRAM-SHA-512)
        """
        return pulumi.get(self, "scram_mechanism")

    @scram_mechanism.setter
    def scram_mechanism(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "scram_mechanism", value)

    @property
    @pulumi.getter
    def username(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the credential
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username", value)


class UserScramCredential(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 scram_iterations: Optional[pulumi.Input[int]] = None,
                 scram_mechanism: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a UserScramCredential resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] password: The password of the credential
        :param pulumi.Input[int] scram_iterations: The number of SCRAM iterations used when generating the credential
        :param pulumi.Input[str] scram_mechanism: The SCRAM mechanism used to generate the credential (SCRAM-SHA-256, SCRAM-SHA-512)
        :param pulumi.Input[str] username: The name of the credential
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UserScramCredentialArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a UserScramCredential resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param UserScramCredentialArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UserScramCredentialArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 scram_iterations: Optional[pulumi.Input[int]] = None,
                 scram_mechanism: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UserScramCredentialArgs.__new__(UserScramCredentialArgs)

            if password is None and not opts.urn:
                raise TypeError("Missing required property 'password'")
            __props__.__dict__["password"] = None if password is None else pulumi.Output.secret(password)
            __props__.__dict__["scram_iterations"] = scram_iterations
            if scram_mechanism is None and not opts.urn:
                raise TypeError("Missing required property 'scram_mechanism'")
            __props__.__dict__["scram_mechanism"] = scram_mechanism
            if username is None and not opts.urn:
                raise TypeError("Missing required property 'username'")
            __props__.__dict__["username"] = username
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["password"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(UserScramCredential, __self__).__init__(
            'kafka:index/userScramCredential:UserScramCredential',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            password: Optional[pulumi.Input[str]] = None,
            scram_iterations: Optional[pulumi.Input[int]] = None,
            scram_mechanism: Optional[pulumi.Input[str]] = None,
            username: Optional[pulumi.Input[str]] = None) -> 'UserScramCredential':
        """
        Get an existing UserScramCredential resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] password: The password of the credential
        :param pulumi.Input[int] scram_iterations: The number of SCRAM iterations used when generating the credential
        :param pulumi.Input[str] scram_mechanism: The SCRAM mechanism used to generate the credential (SCRAM-SHA-256, SCRAM-SHA-512)
        :param pulumi.Input[str] username: The name of the credential
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _UserScramCredentialState.__new__(_UserScramCredentialState)

        __props__.__dict__["password"] = password
        __props__.__dict__["scram_iterations"] = scram_iterations
        __props__.__dict__["scram_mechanism"] = scram_mechanism
        __props__.__dict__["username"] = username
        return UserScramCredential(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def password(self) -> pulumi.Output[str]:
        """
        The password of the credential
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter(name="scramIterations")
    def scram_iterations(self) -> pulumi.Output[Optional[int]]:
        """
        The number of SCRAM iterations used when generating the credential
        """
        return pulumi.get(self, "scram_iterations")

    @property
    @pulumi.getter(name="scramMechanism")
    def scram_mechanism(self) -> pulumi.Output[str]:
        """
        The SCRAM mechanism used to generate the credential (SCRAM-SHA-256, SCRAM-SHA-512)
        """
        return pulumi.get(self, "scram_mechanism")

    @property
    @pulumi.getter
    def username(self) -> pulumi.Output[str]:
        """
        The name of the credential
        """
        return pulumi.get(self, "username")

