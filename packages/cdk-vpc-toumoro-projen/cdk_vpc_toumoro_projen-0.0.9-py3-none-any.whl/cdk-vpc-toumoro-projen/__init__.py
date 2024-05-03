'''
# replace this
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import constructs as _constructs_77d1e7e8


class VpcBase(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-vpc-toumoro-projen.VpcBase",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cidr: builtins.str,
        max_azs: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cidr: 
        :param max_azs: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e3010ee1a172e4b1e59ff3f52ffda9e2c13c33133ed35298483e4ecbad5cb08)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = VpcProps(cidr=cidr, max_azs=max_azs)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.Vpc:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Vpc, jsii.get(self, "vpc"))


@jsii.data_type(
    jsii_type="cdk-vpc-toumoro-projen.VpcProps",
    jsii_struct_bases=[],
    name_mapping={"cidr": "cidr", "max_azs": "maxAzs"},
)
class VpcProps:
    def __init__(
        self,
        *,
        cidr: builtins.str,
        max_azs: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cidr: 
        :param max_azs: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e4ca0a64414ac01f1cb33a9c52cbdf1d6944723ded23e6fbdd5101c0defc3a7)
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument max_azs", value=max_azs, expected_type=type_hints["max_azs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cidr": cidr,
        }
        if max_azs is not None:
            self._values["max_azs"] = max_azs

    @builtins.property
    def cidr(self) -> builtins.str:
        result = self._values.get("cidr")
        assert result is not None, "Required property 'cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_azs(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_azs")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "VpcBase",
    "VpcProps",
]

publication.publish()

def _typecheckingstub__7e3010ee1a172e4b1e59ff3f52ffda9e2c13c33133ed35298483e4ecbad5cb08(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cidr: builtins.str,
    max_azs: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e4ca0a64414ac01f1cb33a9c52cbdf1d6944723ded23e6fbdd5101c0defc3a7(
    *,
    cidr: builtins.str,
    max_azs: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
