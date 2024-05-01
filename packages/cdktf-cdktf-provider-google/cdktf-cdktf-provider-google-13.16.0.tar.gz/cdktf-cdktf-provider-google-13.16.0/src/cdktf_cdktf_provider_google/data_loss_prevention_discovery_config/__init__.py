'''
# `google_data_loss_prevention_discovery_config`

Refer to the Terraform Registry for docs: [`google_data_loss_prevention_discovery_config`](https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config).
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

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class DataLossPreventionDiscoveryConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config google_data_loss_prevention_discovery_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        parent: builtins.str,
        actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionDiscoveryConfigActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        inspect_templates: typing.Optional[typing.Sequence[builtins.str]] = None,
        org_config: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigOrgConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionDiscoveryConfigTargets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config google_data_loss_prevention_discovery_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Location to create the discovery config in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#location DataLossPreventionDiscoveryConfig#location}
        :param parent: The parent of the discovery config in any of the following formats:. - 'projects/{{project}}/locations/{{location}}' - 'organizations/{{organization_id}}/locations/{{location}}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#parent DataLossPreventionDiscoveryConfig#parent}
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#actions DataLossPreventionDiscoveryConfig#actions}
        :param display_name: Display Name (max 1000 Chars). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#display_name DataLossPreventionDiscoveryConfig#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#id DataLossPreventionDiscoveryConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inspect_templates: Detection logic for profile generation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#inspect_templates DataLossPreventionDiscoveryConfig#inspect_templates}
        :param org_config: org_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#org_config DataLossPreventionDiscoveryConfig#org_config}
        :param status: Required. A status for this configuration Possible values: ["RUNNING", "PAUSED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#status DataLossPreventionDiscoveryConfig#status}
        :param targets: targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#targets DataLossPreventionDiscoveryConfig#targets}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#timeouts DataLossPreventionDiscoveryConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__924f5f32f0e280de2745fafbf26e0894a51ebab5e979db1626aa93fb40e973db)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataLossPreventionDiscoveryConfigConfig(
            location=location,
            parent=parent,
            actions=actions,
            display_name=display_name,
            id=id,
            inspect_templates=inspect_templates,
            org_config=org_config,
            status=status,
            targets=targets,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a DataLossPreventionDiscoveryConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataLossPreventionDiscoveryConfig to import.
        :param import_from_id: The id of the existing DataLossPreventionDiscoveryConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataLossPreventionDiscoveryConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3728039a3e9fb7552fe7a7d34a43adeaceeb277b9c34639ea6dede095a2ecd2d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putActions")
    def put_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionDiscoveryConfigActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2389950dd6cf60bf989a25578bf22084cb8f61b41e829a0bef177054e5ff0675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @jsii.member(jsii_name="putOrgConfig")
    def put_org_config(
        self,
        *,
        location: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigOrgConfigLocation", typing.Dict[builtins.str, typing.Any]]] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param location: location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#location DataLossPreventionDiscoveryConfig#location}
        :param project_id: The project that will run the scan. The DLP service account that exists within this project must have access to all resources that are profiled, and the cloud DLP API must be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#project_id DataLossPreventionDiscoveryConfig#project_id}
        '''
        value = DataLossPreventionDiscoveryConfigOrgConfig(
            location=location, project_id=project_id
        )

        return typing.cast(None, jsii.invoke(self, "putOrgConfig", [value]))

    @jsii.member(jsii_name="putTargets")
    def put_targets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionDiscoveryConfigTargets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e1e013e90c699259a9f67aca7da5239d5a0530bf9428ec62619291dfbb6d5f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTargets", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#create DataLossPreventionDiscoveryConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#delete DataLossPreventionDiscoveryConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#update DataLossPreventionDiscoveryConfig#update}.
        '''
        value = DataLossPreventionDiscoveryConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetActions")
    def reset_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActions", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInspectTemplates")
    def reset_inspect_templates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInspectTemplates", []))

    @jsii.member(jsii_name="resetOrgConfig")
    def reset_org_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrgConfig", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetTargets")
    def reset_targets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargets", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> "DataLossPreventionDiscoveryConfigActionsList":
        return typing.cast("DataLossPreventionDiscoveryConfigActionsList", jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="errors")
    def errors(self) -> "DataLossPreventionDiscoveryConfigErrorsList":
        return typing.cast("DataLossPreventionDiscoveryConfigErrorsList", jsii.get(self, "errors"))

    @builtins.property
    @jsii.member(jsii_name="lastRunTime")
    def last_run_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastRunTime"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="orgConfig")
    def org_config(self) -> "DataLossPreventionDiscoveryConfigOrgConfigOutputReference":
        return typing.cast("DataLossPreventionDiscoveryConfigOrgConfigOutputReference", jsii.get(self, "orgConfig"))

    @builtins.property
    @jsii.member(jsii_name="targets")
    def targets(self) -> "DataLossPreventionDiscoveryConfigTargetsList":
        return typing.cast("DataLossPreventionDiscoveryConfigTargetsList", jsii.get(self, "targets"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataLossPreventionDiscoveryConfigTimeoutsOutputReference":
        return typing.cast("DataLossPreventionDiscoveryConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionDiscoveryConfigActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionDiscoveryConfigActions"]]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inspectTemplatesInput")
    def inspect_templates_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inspectTemplatesInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="orgConfigInput")
    def org_config_input(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigOrgConfig"]:
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigOrgConfig"], jsii.get(self, "orgConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="targetsInput")
    def targets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionDiscoveryConfigTargets"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionDiscoveryConfigTargets"]]], jsii.get(self, "targetsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataLossPreventionDiscoveryConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataLossPreventionDiscoveryConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f41df159678b11c6ebb6c29be22808b75d745e4c9f296b5b612be64896a2eb1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b26a6e8081293d8ff39aca03b13abe4b3bc2bf5b741f8da4155bb03d19235e75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="inspectTemplates")
    def inspect_templates(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inspectTemplates"))

    @inspect_templates.setter
    def inspect_templates(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d67cff7986a9a806af85f1407a33812c9f6f5db3289311c3f74a0529516aa28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inspectTemplates", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52a1431eb31ed73181d36e6e5cccfca570d4b9f614be1255d1d493c46b4a8044)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67d57fc28039fa32ba3f027e575bb7a7778c9234638e0542e1f36f5b9f6fccee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70503977e85bce9405e07fd9d51a6a35de34e8e16950d19dfee45f4e9d7819cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigActions",
    jsii_struct_bases=[],
    name_mapping={
        "export_data": "exportData",
        "pub_sub_notification": "pubSubNotification",
    },
)
class DataLossPreventionDiscoveryConfigActions:
    def __init__(
        self,
        *,
        export_data: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigActionsExportData", typing.Dict[builtins.str, typing.Any]]] = None,
        pub_sub_notification: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigActionsPubSubNotification", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param export_data: export_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#export_data DataLossPreventionDiscoveryConfig#export_data}
        :param pub_sub_notification: pub_sub_notification block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#pub_sub_notification DataLossPreventionDiscoveryConfig#pub_sub_notification}
        '''
        if isinstance(export_data, dict):
            export_data = DataLossPreventionDiscoveryConfigActionsExportData(**export_data)
        if isinstance(pub_sub_notification, dict):
            pub_sub_notification = DataLossPreventionDiscoveryConfigActionsPubSubNotification(**pub_sub_notification)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abbf47bb422d1bf869b0f79983405cf854e4aec17fb82afad6175df327fe0eb3)
            check_type(argname="argument export_data", value=export_data, expected_type=type_hints["export_data"])
            check_type(argname="argument pub_sub_notification", value=pub_sub_notification, expected_type=type_hints["pub_sub_notification"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if export_data is not None:
            self._values["export_data"] = export_data
        if pub_sub_notification is not None:
            self._values["pub_sub_notification"] = pub_sub_notification

    @builtins.property
    def export_data(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigActionsExportData"]:
        '''export_data block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#export_data DataLossPreventionDiscoveryConfig#export_data}
        '''
        result = self._values.get("export_data")
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigActionsExportData"], result)

    @builtins.property
    def pub_sub_notification(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigActionsPubSubNotification"]:
        '''pub_sub_notification block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#pub_sub_notification DataLossPreventionDiscoveryConfig#pub_sub_notification}
        '''
        result = self._values.get("pub_sub_notification")
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigActionsPubSubNotification"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigActionsExportData",
    jsii_struct_bases=[],
    name_mapping={"profile_table": "profileTable"},
)
class DataLossPreventionDiscoveryConfigActionsExportData:
    def __init__(
        self,
        *,
        profile_table: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigActionsExportDataProfileTable", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param profile_table: profile_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#profile_table DataLossPreventionDiscoveryConfig#profile_table}
        '''
        if isinstance(profile_table, dict):
            profile_table = DataLossPreventionDiscoveryConfigActionsExportDataProfileTable(**profile_table)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44c87ac9f2d6015bc04d9029f4cebbdac66e81de8bee4ccdfc31fa118a8efe8c)
            check_type(argname="argument profile_table", value=profile_table, expected_type=type_hints["profile_table"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if profile_table is not None:
            self._values["profile_table"] = profile_table

    @builtins.property
    def profile_table(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigActionsExportDataProfileTable"]:
        '''profile_table block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#profile_table DataLossPreventionDiscoveryConfig#profile_table}
        '''
        result = self._values.get("profile_table")
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigActionsExportDataProfileTable"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigActionsExportData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDiscoveryConfigActionsExportDataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigActionsExportDataOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ebcf4906c00116b97dc8dffc7dda631500b64a496d944e2383dde5b51cdfe78)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProfileTable")
    def put_profile_table(
        self,
        *,
        dataset_id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        table_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataset_id: Dataset Id of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#dataset_id DataLossPreventionDiscoveryConfig#dataset_id}
        :param project_id: The Google Cloud Platform project ID of the project containing the table. If omitted, the project ID is inferred from the API call. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#project_id DataLossPreventionDiscoveryConfig#project_id}
        :param table_id: Name of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#table_id DataLossPreventionDiscoveryConfig#table_id}
        '''
        value = DataLossPreventionDiscoveryConfigActionsExportDataProfileTable(
            dataset_id=dataset_id, project_id=project_id, table_id=table_id
        )

        return typing.cast(None, jsii.invoke(self, "putProfileTable", [value]))

    @jsii.member(jsii_name="resetProfileTable")
    def reset_profile_table(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProfileTable", []))

    @builtins.property
    @jsii.member(jsii_name="profileTable")
    def profile_table(
        self,
    ) -> "DataLossPreventionDiscoveryConfigActionsExportDataProfileTableOutputReference":
        return typing.cast("DataLossPreventionDiscoveryConfigActionsExportDataProfileTableOutputReference", jsii.get(self, "profileTable"))

    @builtins.property
    @jsii.member(jsii_name="profileTableInput")
    def profile_table_input(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigActionsExportDataProfileTable"]:
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigActionsExportDataProfileTable"], jsii.get(self, "profileTableInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigActionsExportData]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigActionsExportData], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDiscoveryConfigActionsExportData],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a85769cd0134c9b9c7e4e7902c758b5b4cc1ccc61d909554359c94e8339e7cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigActionsExportDataProfileTable",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_id": "datasetId",
        "project_id": "projectId",
        "table_id": "tableId",
    },
)
class DataLossPreventionDiscoveryConfigActionsExportDataProfileTable:
    def __init__(
        self,
        *,
        dataset_id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        table_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataset_id: Dataset Id of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#dataset_id DataLossPreventionDiscoveryConfig#dataset_id}
        :param project_id: The Google Cloud Platform project ID of the project containing the table. If omitted, the project ID is inferred from the API call. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#project_id DataLossPreventionDiscoveryConfig#project_id}
        :param table_id: Name of the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#table_id DataLossPreventionDiscoveryConfig#table_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6b491b82e7553868750436b2f05c5396758bb67255a4bf1f4c4f13866ea886d)
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dataset_id is not None:
            self._values["dataset_id"] = dataset_id
        if project_id is not None:
            self._values["project_id"] = project_id
        if table_id is not None:
            self._values["table_id"] = table_id

    @builtins.property
    def dataset_id(self) -> typing.Optional[builtins.str]:
        '''Dataset Id of the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#dataset_id DataLossPreventionDiscoveryConfig#dataset_id}
        '''
        result = self._values.get("dataset_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The Google Cloud Platform project ID of the project containing the table.

        If omitted, the project ID is inferred from the API call.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#project_id DataLossPreventionDiscoveryConfig#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_id(self) -> typing.Optional[builtins.str]:
        '''Name of the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#table_id DataLossPreventionDiscoveryConfig#table_id}
        '''
        result = self._values.get("table_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigActionsExportDataProfileTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDiscoveryConfigActionsExportDataProfileTableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigActionsExportDataProfileTableOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc5f34b90a3f82e80c47de5455697a035e9ae0859f39022de8bfa2adff03474)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDatasetId")
    def reset_dataset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatasetId", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetTableId")
    def reset_table_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTableId", []))

    @builtins.property
    @jsii.member(jsii_name="datasetIdInput")
    def dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tableIdInput")
    def table_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableIdInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetId"))

    @dataset_id.setter
    def dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__581c9a28645744cdfd16b58e49bbd338f835e92eff330aa8bcbeacd33184b2a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value)

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad7b411ebc23df6d9ebaf68a04c8de4e2e90883674f95cc66ab2dd97a020199c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value)

    @builtins.property
    @jsii.member(jsii_name="tableId")
    def table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableId"))

    @table_id.setter
    def table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0930f6d0d54c6fe6726697859dabae0cedd145fc07243d4ed88a29c2b6b6ece7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigActionsExportDataProfileTable]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigActionsExportDataProfileTable], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDiscoveryConfigActionsExportDataProfileTable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb6d337100de3ed5c896aba914baf26f9cb7833f3b4c3b8a210c3e093aacbc12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDiscoveryConfigActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigActionsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__889d51e590628191311c60e9d2b9dc2597af60dc90f9f6a49afaec481be08906)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionDiscoveryConfigActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__562ccde911d8e4f3b485f43463a0cb052ecd996e82fccfa3346e1f145288cf16)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionDiscoveryConfigActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__478c9722145420d26173e94f82f7c8226d2e51711b9ccd1f8e2b66998d4afc6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__388063a6904c5e55becd13a666ec6339e1b9e0d9ac94613383fd17ad328c3ec4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b928291d85b3df2052a5b67b92d545dd5ea83093f5797b65079b1e3482b9c442)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDiscoveryConfigActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDiscoveryConfigActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDiscoveryConfigActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f53bfd93997d171f41af215faf10920dbbfa81ff33042f30f83830a382fbd87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDiscoveryConfigActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigActionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acb52dbca95654cdd9b16920290763c8c0a5798ddef2491d7d96215fe063c6ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putExportData")
    def put_export_data(
        self,
        *,
        profile_table: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigActionsExportDataProfileTable, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param profile_table: profile_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#profile_table DataLossPreventionDiscoveryConfig#profile_table}
        '''
        value = DataLossPreventionDiscoveryConfigActionsExportData(
            profile_table=profile_table
        )

        return typing.cast(None, jsii.invoke(self, "putExportData", [value]))

    @jsii.member(jsii_name="putPubSubNotification")
    def put_pub_sub_notification(
        self,
        *,
        detail_of_message: typing.Optional[builtins.str] = None,
        event: typing.Optional[builtins.str] = None,
        pubsub_condition: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        topic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param detail_of_message: How much data to include in the pub/sub message. Possible values: ["TABLE_PROFILE", "RESOURCE_NAME"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#detail_of_message DataLossPreventionDiscoveryConfig#detail_of_message}
        :param event: The type of event that triggers a Pub/Sub. At most one PubSubNotification per EventType is permitted. Possible values: ["NEW_PROFILE", "CHANGED_PROFILE", "SCORE_INCREASED", "ERROR_CHANGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#event DataLossPreventionDiscoveryConfig#event}
        :param pubsub_condition: pubsub_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#pubsub_condition DataLossPreventionDiscoveryConfig#pubsub_condition}
        :param topic: Cloud Pub/Sub topic to send notifications to. Format is projects/{project}/topics/{topic}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#topic DataLossPreventionDiscoveryConfig#topic}
        '''
        value = DataLossPreventionDiscoveryConfigActionsPubSubNotification(
            detail_of_message=detail_of_message,
            event=event,
            pubsub_condition=pubsub_condition,
            topic=topic,
        )

        return typing.cast(None, jsii.invoke(self, "putPubSubNotification", [value]))

    @jsii.member(jsii_name="resetExportData")
    def reset_export_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportData", []))

    @jsii.member(jsii_name="resetPubSubNotification")
    def reset_pub_sub_notification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPubSubNotification", []))

    @builtins.property
    @jsii.member(jsii_name="exportData")
    def export_data(
        self,
    ) -> DataLossPreventionDiscoveryConfigActionsExportDataOutputReference:
        return typing.cast(DataLossPreventionDiscoveryConfigActionsExportDataOutputReference, jsii.get(self, "exportData"))

    @builtins.property
    @jsii.member(jsii_name="pubSubNotification")
    def pub_sub_notification(
        self,
    ) -> "DataLossPreventionDiscoveryConfigActionsPubSubNotificationOutputReference":
        return typing.cast("DataLossPreventionDiscoveryConfigActionsPubSubNotificationOutputReference", jsii.get(self, "pubSubNotification"))

    @builtins.property
    @jsii.member(jsii_name="exportDataInput")
    def export_data_input(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigActionsExportData]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigActionsExportData], jsii.get(self, "exportDataInput"))

    @builtins.property
    @jsii.member(jsii_name="pubSubNotificationInput")
    def pub_sub_notification_input(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigActionsPubSubNotification"]:
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigActionsPubSubNotification"], jsii.get(self, "pubSubNotificationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionDiscoveryConfigActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionDiscoveryConfigActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionDiscoveryConfigActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdadcb3cf5a1adb677ac8d6b6a27040c7c31646d6fe6f0b2188b8f59cad22beb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigActionsPubSubNotification",
    jsii_struct_bases=[],
    name_mapping={
        "detail_of_message": "detailOfMessage",
        "event": "event",
        "pubsub_condition": "pubsubCondition",
        "topic": "topic",
    },
)
class DataLossPreventionDiscoveryConfigActionsPubSubNotification:
    def __init__(
        self,
        *,
        detail_of_message: typing.Optional[builtins.str] = None,
        event: typing.Optional[builtins.str] = None,
        pubsub_condition: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        topic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param detail_of_message: How much data to include in the pub/sub message. Possible values: ["TABLE_PROFILE", "RESOURCE_NAME"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#detail_of_message DataLossPreventionDiscoveryConfig#detail_of_message}
        :param event: The type of event that triggers a Pub/Sub. At most one PubSubNotification per EventType is permitted. Possible values: ["NEW_PROFILE", "CHANGED_PROFILE", "SCORE_INCREASED", "ERROR_CHANGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#event DataLossPreventionDiscoveryConfig#event}
        :param pubsub_condition: pubsub_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#pubsub_condition DataLossPreventionDiscoveryConfig#pubsub_condition}
        :param topic: Cloud Pub/Sub topic to send notifications to. Format is projects/{project}/topics/{topic}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#topic DataLossPreventionDiscoveryConfig#topic}
        '''
        if isinstance(pubsub_condition, dict):
            pubsub_condition = DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition(**pubsub_condition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc76bc5bdd470fec76011737252b713061f6efc2a65798b309e2a7092b944b5a)
            check_type(argname="argument detail_of_message", value=detail_of_message, expected_type=type_hints["detail_of_message"])
            check_type(argname="argument event", value=event, expected_type=type_hints["event"])
            check_type(argname="argument pubsub_condition", value=pubsub_condition, expected_type=type_hints["pubsub_condition"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if detail_of_message is not None:
            self._values["detail_of_message"] = detail_of_message
        if event is not None:
            self._values["event"] = event
        if pubsub_condition is not None:
            self._values["pubsub_condition"] = pubsub_condition
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def detail_of_message(self) -> typing.Optional[builtins.str]:
        '''How much data to include in the pub/sub message. Possible values: ["TABLE_PROFILE", "RESOURCE_NAME"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#detail_of_message DataLossPreventionDiscoveryConfig#detail_of_message}
        '''
        result = self._values.get("detail_of_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event(self) -> typing.Optional[builtins.str]:
        '''The type of event that triggers a Pub/Sub.

        At most one PubSubNotification per EventType is permitted. Possible values: ["NEW_PROFILE", "CHANGED_PROFILE", "SCORE_INCREASED", "ERROR_CHANGED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#event DataLossPreventionDiscoveryConfig#event}
        '''
        result = self._values.get("event")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pubsub_condition(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition"]:
        '''pubsub_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#pubsub_condition DataLossPreventionDiscoveryConfig#pubsub_condition}
        '''
        result = self._values.get("pubsub_condition")
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition"], result)

    @builtins.property
    def topic(self) -> typing.Optional[builtins.str]:
        '''Cloud Pub/Sub topic to send notifications to. Format is projects/{project}/topics/{topic}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#topic DataLossPreventionDiscoveryConfig#topic}
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigActionsPubSubNotification(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDiscoveryConfigActionsPubSubNotificationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigActionsPubSubNotificationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__040aa220bf8287cdb5a4edf4cf649331b070d199d1f03583c4e80addc65e11a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPubsubCondition")
    def put_pubsub_condition(
        self,
        *,
        expressions: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param expressions: expressions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#expressions DataLossPreventionDiscoveryConfig#expressions}
        '''
        value = DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition(
            expressions=expressions
        )

        return typing.cast(None, jsii.invoke(self, "putPubsubCondition", [value]))

    @jsii.member(jsii_name="resetDetailOfMessage")
    def reset_detail_of_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDetailOfMessage", []))

    @jsii.member(jsii_name="resetEvent")
    def reset_event(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvent", []))

    @jsii.member(jsii_name="resetPubsubCondition")
    def reset_pubsub_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPubsubCondition", []))

    @jsii.member(jsii_name="resetTopic")
    def reset_topic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopic", []))

    @builtins.property
    @jsii.member(jsii_name="pubsubCondition")
    def pubsub_condition(
        self,
    ) -> "DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionOutputReference":
        return typing.cast("DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionOutputReference", jsii.get(self, "pubsubCondition"))

    @builtins.property
    @jsii.member(jsii_name="detailOfMessageInput")
    def detail_of_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "detailOfMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="eventInput")
    def event_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventInput"))

    @builtins.property
    @jsii.member(jsii_name="pubsubConditionInput")
    def pubsub_condition_input(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition"]:
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition"], jsii.get(self, "pubsubConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="detailOfMessage")
    def detail_of_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "detailOfMessage"))

    @detail_of_message.setter
    def detail_of_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7201f77cb19f42683379d00539956b2adc9c1aa25edb9df3f3f7aecbdbe6d2bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detailOfMessage", value)

    @builtins.property
    @jsii.member(jsii_name="event")
    def event(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "event"))

    @event.setter
    def event(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f75288df0d650d2e0c8ea1725f0d32e4432a61d9429d4a5290670e9f45d218f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "event", value)

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__860856839e112139630e606bd01911b571aca115afb2728514929a94f97f3e87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigActionsPubSubNotification]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigActionsPubSubNotification], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDiscoveryConfigActionsPubSubNotification],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__522c9121a119f67b7d20a9067c679d5b3ea2bab8281678fc8e12fc6495fca66b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition",
    jsii_struct_bases=[],
    name_mapping={"expressions": "expressions"},
)
class DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition:
    def __init__(
        self,
        *,
        expressions: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param expressions: expressions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#expressions DataLossPreventionDiscoveryConfig#expressions}
        '''
        if isinstance(expressions, dict):
            expressions = DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions(**expressions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__318e569ab7f37f28fb99d2b6f03e7520ff926ba64827946a4c9a156faf827e43)
            check_type(argname="argument expressions", value=expressions, expected_type=type_hints["expressions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if expressions is not None:
            self._values["expressions"] = expressions

    @builtins.property
    def expressions(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions"]:
        '''expressions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#expressions DataLossPreventionDiscoveryConfig#expressions}
        '''
        result = self._values.get("expressions")
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions",
    jsii_struct_bases=[],
    name_mapping={"conditions": "conditions", "logical_operator": "logicalOperator"},
)
class DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions:
    def __init__(
        self,
        *,
        conditions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        logical_operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#conditions DataLossPreventionDiscoveryConfig#conditions}
        :param logical_operator: The operator to apply to the collection of conditions Possible values: ["OR", "AND"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#logical_operator DataLossPreventionDiscoveryConfig#logical_operator}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d91930a29ec146016a3307a15037398decbf03a33f022480d6fc36ad2d279213)
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument logical_operator", value=logical_operator, expected_type=type_hints["logical_operator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if conditions is not None:
            self._values["conditions"] = conditions
        if logical_operator is not None:
            self._values["logical_operator"] = logical_operator

    @builtins.property
    def conditions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions"]]]:
        '''conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#conditions DataLossPreventionDiscoveryConfig#conditions}
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions"]]], result)

    @builtins.property
    def logical_operator(self) -> typing.Optional[builtins.str]:
        '''The operator to apply to the collection of conditions Possible values: ["OR", "AND"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#logical_operator DataLossPreventionDiscoveryConfig#logical_operator}
        '''
        result = self._values.get("logical_operator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions",
    jsii_struct_bases=[],
    name_mapping={
        "minimum_risk_score": "minimumRiskScore",
        "minimum_sensitivity_score": "minimumSensitivityScore",
    },
)
class DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions:
    def __init__(
        self,
        *,
        minimum_risk_score: typing.Optional[builtins.str] = None,
        minimum_sensitivity_score: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param minimum_risk_score: The minimum data risk score that triggers the condition. Possible values: ["HIGH", "MEDIUM_OR_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#minimum_risk_score DataLossPreventionDiscoveryConfig#minimum_risk_score}
        :param minimum_sensitivity_score: The minimum sensitivity level that triggers the condition. Possible values: ["HIGH", "MEDIUM_OR_HIGH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#minimum_sensitivity_score DataLossPreventionDiscoveryConfig#minimum_sensitivity_score}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3017106ee249b9a7bb2fbf201541b57a5060880f0c3dff0d29eb4be83cef0838)
            check_type(argname="argument minimum_risk_score", value=minimum_risk_score, expected_type=type_hints["minimum_risk_score"])
            check_type(argname="argument minimum_sensitivity_score", value=minimum_sensitivity_score, expected_type=type_hints["minimum_sensitivity_score"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if minimum_risk_score is not None:
            self._values["minimum_risk_score"] = minimum_risk_score
        if minimum_sensitivity_score is not None:
            self._values["minimum_sensitivity_score"] = minimum_sensitivity_score

    @builtins.property
    def minimum_risk_score(self) -> typing.Optional[builtins.str]:
        '''The minimum data risk score that triggers the condition. Possible values: ["HIGH", "MEDIUM_OR_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#minimum_risk_score DataLossPreventionDiscoveryConfig#minimum_risk_score}
        '''
        result = self._values.get("minimum_risk_score")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimum_sensitivity_score(self) -> typing.Optional[builtins.str]:
        '''The minimum sensitivity level that triggers the condition. Possible values: ["HIGH", "MEDIUM_OR_HIGH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#minimum_sensitivity_score DataLossPreventionDiscoveryConfig#minimum_sensitivity_score}
        '''
        result = self._values.get("minimum_sensitivity_score")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditionsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c5e556cb2478107dce90e6f9fbed84c8c9aef274c8320705f619c46825eff40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__608ad0370b3015495cda3f34c5a991c5ca78339f1f2c268f04167b96a1841d1e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac7215973cca6c562be70df17f179add306f7dd9d86b74911c3b15a158ed4c1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7cee11e11bf6a5ca6e454c8d8f5592c5c75bdfe3e1d5df83c36a98a1504d1be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce0a6feee4aaa57943d639ffd99645aae4fb7ca1717c0180976e3a6b517c5dcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3146ac4198c9e0deb2333342c65d6a73675e90037a24d11b5184788d1457993c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ad33fe57fa6b8c99cab2f248e16675b29afad0a9f1ccc8939f6d7954eb254bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMinimumRiskScore")
    def reset_minimum_risk_score(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumRiskScore", []))

    @jsii.member(jsii_name="resetMinimumSensitivityScore")
    def reset_minimum_sensitivity_score(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumSensitivityScore", []))

    @builtins.property
    @jsii.member(jsii_name="minimumRiskScoreInput")
    def minimum_risk_score_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimumRiskScoreInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumSensitivityScoreInput")
    def minimum_sensitivity_score_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimumSensitivityScoreInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumRiskScore")
    def minimum_risk_score(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimumRiskScore"))

    @minimum_risk_score.setter
    def minimum_risk_score(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f41ace3d0721b70051c6552fa6943b6a094cf62645ee5ae6158eaa5c93fcdffe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumRiskScore", value)

    @builtins.property
    @jsii.member(jsii_name="minimumSensitivityScore")
    def minimum_sensitivity_score(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimumSensitivityScore"))

    @minimum_sensitivity_score.setter
    def minimum_sensitivity_score(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__856086e455e10c4216aecf6601223ce0801610d0602f774b8e3a2d71b408b234)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumSensitivityScore", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3380741e979701127e6656bddef5db508b86150f4e11a22eedfb01165ab59ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a01c3db3effb217f991b2d1c311f5cc51ab600a9869390f2a93783c9a8baad7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConditions")
    def put_conditions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e73ea8ac49b4eef34857d0eca4cf935d18ab70ca11b2facc21b0949165bd6fa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConditions", [value]))

    @jsii.member(jsii_name="resetConditions")
    def reset_conditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditions", []))

    @jsii.member(jsii_name="resetLogicalOperator")
    def reset_logical_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogicalOperator", []))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(
        self,
    ) -> DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditionsList:
        return typing.cast(DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="conditionsInput")
    def conditions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions]]], jsii.get(self, "conditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="logicalOperatorInput")
    def logical_operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logicalOperatorInput"))

    @builtins.property
    @jsii.member(jsii_name="logicalOperator")
    def logical_operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logicalOperator"))

    @logical_operator.setter
    def logical_operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2afc2226dafa0b67ff21c6a3a1d59c56a54c05c92cc341526f3dc7b1831bd461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logicalOperator", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5430fd65e1a93059a6456ae70dbf2258d9ce62d80e171a27e6894be6d5b59a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03d690419caf93a8c62ac0411bf154f1a6192869bd398a422a98292886584d40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExpressions")
    def put_expressions(
        self,
        *,
        conditions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions, typing.Dict[builtins.str, typing.Any]]]]] = None,
        logical_operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#conditions DataLossPreventionDiscoveryConfig#conditions}
        :param logical_operator: The operator to apply to the collection of conditions Possible values: ["OR", "AND"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#logical_operator DataLossPreventionDiscoveryConfig#logical_operator}
        '''
        value = DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions(
            conditions=conditions, logical_operator=logical_operator
        )

        return typing.cast(None, jsii.invoke(self, "putExpressions", [value]))

    @jsii.member(jsii_name="resetExpressions")
    def reset_expressions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpressions", []))

    @builtins.property
    @jsii.member(jsii_name="expressions")
    def expressions(
        self,
    ) -> DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsOutputReference:
        return typing.cast(DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsOutputReference, jsii.get(self, "expressions"))

    @builtins.property
    @jsii.member(jsii_name="expressionsInput")
    def expressions_input(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions], jsii.get(self, "expressionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60a13a9d02ddb6495b98117d3b5bd7a59f09ed49c78a7c4ecfef6a6e63bcdfb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "parent": "parent",
        "actions": "actions",
        "display_name": "displayName",
        "id": "id",
        "inspect_templates": "inspectTemplates",
        "org_config": "orgConfig",
        "status": "status",
        "targets": "targets",
        "timeouts": "timeouts",
    },
)
class DataLossPreventionDiscoveryConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        location: builtins.str,
        parent: builtins.str,
        actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDiscoveryConfigActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        inspect_templates: typing.Optional[typing.Sequence[builtins.str]] = None,
        org_config: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigOrgConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionDiscoveryConfigTargets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Location to create the discovery config in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#location DataLossPreventionDiscoveryConfig#location}
        :param parent: The parent of the discovery config in any of the following formats:. - 'projects/{{project}}/locations/{{location}}' - 'organizations/{{organization_id}}/locations/{{location}}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#parent DataLossPreventionDiscoveryConfig#parent}
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#actions DataLossPreventionDiscoveryConfig#actions}
        :param display_name: Display Name (max 1000 Chars). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#display_name DataLossPreventionDiscoveryConfig#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#id DataLossPreventionDiscoveryConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inspect_templates: Detection logic for profile generation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#inspect_templates DataLossPreventionDiscoveryConfig#inspect_templates}
        :param org_config: org_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#org_config DataLossPreventionDiscoveryConfig#org_config}
        :param status: Required. A status for this configuration Possible values: ["RUNNING", "PAUSED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#status DataLossPreventionDiscoveryConfig#status}
        :param targets: targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#targets DataLossPreventionDiscoveryConfig#targets}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#timeouts DataLossPreventionDiscoveryConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(org_config, dict):
            org_config = DataLossPreventionDiscoveryConfigOrgConfig(**org_config)
        if isinstance(timeouts, dict):
            timeouts = DataLossPreventionDiscoveryConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84e6d090ed62c91d71fb43bb299767dee5f0f87529ceb0e6a0255fc12d82107b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument inspect_templates", value=inspect_templates, expected_type=type_hints["inspect_templates"])
            check_type(argname="argument org_config", value=org_config, expected_type=type_hints["org_config"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "parent": parent,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if actions is not None:
            self._values["actions"] = actions
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if inspect_templates is not None:
            self._values["inspect_templates"] = inspect_templates
        if org_config is not None:
            self._values["org_config"] = org_config
        if status is not None:
            self._values["status"] = status
        if targets is not None:
            self._values["targets"] = targets
        if timeouts is not None:
            self._values["timeouts"] = timeouts

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Location to create the discovery config in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#location DataLossPreventionDiscoveryConfig#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parent(self) -> builtins.str:
        '''The parent of the discovery config in any of the following formats:.

        - 'projects/{{project}}/locations/{{location}}'
        - 'organizations/{{organization_id}}/locations/{{location}}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#parent DataLossPreventionDiscoveryConfig#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDiscoveryConfigActions]]]:
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#actions DataLossPreventionDiscoveryConfig#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDiscoveryConfigActions]]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Display Name (max 1000 Chars).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#display_name DataLossPreventionDiscoveryConfig#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#id DataLossPreventionDiscoveryConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inspect_templates(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Detection logic for profile generation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#inspect_templates DataLossPreventionDiscoveryConfig#inspect_templates}
        '''
        result = self._values.get("inspect_templates")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def org_config(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigOrgConfig"]:
        '''org_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#org_config DataLossPreventionDiscoveryConfig#org_config}
        '''
        result = self._values.get("org_config")
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigOrgConfig"], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Required. A status for this configuration Possible values: ["RUNNING", "PAUSED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#status DataLossPreventionDiscoveryConfig#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def targets(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionDiscoveryConfigTargets"]]]:
        '''targets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#targets DataLossPreventionDiscoveryConfig#targets}
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionDiscoveryConfigTargets"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataLossPreventionDiscoveryConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#timeouts DataLossPreventionDiscoveryConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigErrors",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataLossPreventionDiscoveryConfigErrors:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigErrors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigErrorsDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataLossPreventionDiscoveryConfigErrorsDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigErrorsDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDiscoveryConfigErrorsDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigErrorsDetailsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55973b60c05c1a8e8744f19cfd627143eb6769e3cc2dcffc43751c49aa8c472b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionDiscoveryConfigErrorsDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdebc0d2ec300d7d169bfd455b5cc405a61a894edd0354b6ad4ab177fba18f2d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionDiscoveryConfigErrorsDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f462f36128c549d112f0b9723bb9d7d865df8c41710c002e4cb6e80b5d1569f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f8f443c606a04f9de1cbb4f9ae94b00fc89ad2354b78a713d98f87a37d70068)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aebffa7e2ef9faf4a8277cfb517ff48e143367916b79d50bb05fd74464dd18f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataLossPreventionDiscoveryConfigErrorsDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigErrorsDetailsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef32744ede8fdd27a66957b2aae0c90803540e1abfbbb57b3fb3f7cefa9c1d9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "code"))

    @builtins.property
    @jsii.member(jsii_name="details")
    def details(self) -> _cdktf_9a9027ec.StringMapList:
        return typing.cast(_cdktf_9a9027ec.StringMapList, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigErrorsDetails]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigErrorsDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDiscoveryConfigErrorsDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__029d17cfecd2b2b6595d229533817faa05d4466a7b7905f416b459d7299f8f8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDiscoveryConfigErrorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigErrorsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8680e0751404563cc546babe860c24c41a8862a1a2a60f661afe340a3ebfe7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionDiscoveryConfigErrorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5983ab23aef9842facfbe2b8aefc9d961c7e4685cbea1939ab1383fe782ef36)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionDiscoveryConfigErrorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7613249358d3a49fb12cd4c9f06cd8e7849639ff34c36bfdd99e3c1b52df4d79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e66bc7d89c9cd027a4347cd5e043feb67be97a7ac8ae1699e08c16f0a353d449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a549a3f37a98cadbcb674df76e149704b65fe59703943603d80d0502d488a2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataLossPreventionDiscoveryConfigErrorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigErrorsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14c3f2dca41b85dad1ac6885a3b0d4cf0855bd7f71248018f851628860ff6ae4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="details")
    def details(self) -> DataLossPreventionDiscoveryConfigErrorsDetailsList:
        return typing.cast(DataLossPreventionDiscoveryConfigErrorsDetailsList, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="timestamp")
    def timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestamp"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigErrors]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigErrors], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDiscoveryConfigErrors],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fb8327c35adaba6defd93bdc84816bde7c559bafc3de6fc2c9ef50158e76bd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigOrgConfig",
    jsii_struct_bases=[],
    name_mapping={"location": "location", "project_id": "projectId"},
)
class DataLossPreventionDiscoveryConfigOrgConfig:
    def __init__(
        self,
        *,
        location: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigOrgConfigLocation", typing.Dict[builtins.str, typing.Any]]] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param location: location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#location DataLossPreventionDiscoveryConfig#location}
        :param project_id: The project that will run the scan. The DLP service account that exists within this project must have access to all resources that are profiled, and the cloud DLP API must be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#project_id DataLossPreventionDiscoveryConfig#project_id}
        '''
        if isinstance(location, dict):
            location = DataLossPreventionDiscoveryConfigOrgConfigLocation(**location)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5797e1afb754ba6fa0edb772e39d02f5cb4e231af6adc712a13fe7bebcdf049)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if location is not None:
            self._values["location"] = location
        if project_id is not None:
            self._values["project_id"] = project_id

    @builtins.property
    def location(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigOrgConfigLocation"]:
        '''location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#location DataLossPreventionDiscoveryConfig#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigOrgConfigLocation"], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The project that will run the scan.

        The DLP service account that exists within this project must have access to all resources that are profiled, and the cloud DLP API must be enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#project_id DataLossPreventionDiscoveryConfig#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigOrgConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigOrgConfigLocation",
    jsii_struct_bases=[],
    name_mapping={"folder_id": "folderId", "organization_id": "organizationId"},
)
class DataLossPreventionDiscoveryConfigOrgConfigLocation:
    def __init__(
        self,
        *,
        folder_id: typing.Optional[builtins.str] = None,
        organization_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param folder_id: The ID for the folder within an organization to scan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#folder_id DataLossPreventionDiscoveryConfig#folder_id}
        :param organization_id: The ID of an organization to scan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#organization_id DataLossPreventionDiscoveryConfig#organization_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7770781334409fec5e37cb8eaa71a3ca1cb3dfe04734719b2642ed4e026b43a)
            check_type(argname="argument folder_id", value=folder_id, expected_type=type_hints["folder_id"])
            check_type(argname="argument organization_id", value=organization_id, expected_type=type_hints["organization_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if folder_id is not None:
            self._values["folder_id"] = folder_id
        if organization_id is not None:
            self._values["organization_id"] = organization_id

    @builtins.property
    def folder_id(self) -> typing.Optional[builtins.str]:
        '''The ID for the folder within an organization to scan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#folder_id DataLossPreventionDiscoveryConfig#folder_id}
        '''
        result = self._values.get("folder_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization_id(self) -> typing.Optional[builtins.str]:
        '''The ID of an organization to scan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#organization_id DataLossPreventionDiscoveryConfig#organization_id}
        '''
        result = self._values.get("organization_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigOrgConfigLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDiscoveryConfigOrgConfigLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigOrgConfigLocationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad26746672d6f5e1220e87653a91b1c98b51a2a098adae0319f1c185d148b2da)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFolderId")
    def reset_folder_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFolderId", []))

    @jsii.member(jsii_name="resetOrganizationId")
    def reset_organization_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganizationId", []))

    @builtins.property
    @jsii.member(jsii_name="folderIdInput")
    def folder_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "folderIdInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationIdInput")
    def organization_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="folderId")
    def folder_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "folderId"))

    @folder_id.setter
    def folder_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dea563687616e8652054f89c81d4b64fb8715adc16435612cf199b6e40a3f59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "folderId", value)

    @builtins.property
    @jsii.member(jsii_name="organizationId")
    def organization_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationId"))

    @organization_id.setter
    def organization_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43dabdde74b6ba81c8ffec486876826ab588d242f59ae6dab65ba9bec47039b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigOrgConfigLocation]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigOrgConfigLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDiscoveryConfigOrgConfigLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b3b618189597c00fe40d014a23cd25117e4f266a41c3c502d209cbacad8cc41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDiscoveryConfigOrgConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigOrgConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98b45417518f048225935fe61039200bd76e01ee73caa43cea1ce3d55703fc14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLocation")
    def put_location(
        self,
        *,
        folder_id: typing.Optional[builtins.str] = None,
        organization_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param folder_id: The ID for the folder within an organization to scan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#folder_id DataLossPreventionDiscoveryConfig#folder_id}
        :param organization_id: The ID of an organization to scan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#organization_id DataLossPreventionDiscoveryConfig#organization_id}
        '''
        value = DataLossPreventionDiscoveryConfigOrgConfigLocation(
            folder_id=folder_id, organization_id=organization_id
        )

        return typing.cast(None, jsii.invoke(self, "putLocation", [value]))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(
        self,
    ) -> DataLossPreventionDiscoveryConfigOrgConfigLocationOutputReference:
        return typing.cast(DataLossPreventionDiscoveryConfigOrgConfigLocationOutputReference, jsii.get(self, "location"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigOrgConfigLocation]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigOrgConfigLocation], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__269718db80ed33aac34de0dfc58893d46b474be380dab1640979b89ddc003082)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigOrgConfig]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigOrgConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDiscoveryConfigOrgConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df3468ab24efc3720702dc04403f89f028c597d3ae0603a8eadb5ac8435c6877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargets",
    jsii_struct_bases=[],
    name_mapping={"big_query_target": "bigQueryTarget"},
)
class DataLossPreventionDiscoveryConfigTargets:
    def __init__(
        self,
        *,
        big_query_target: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigTargetsBigQueryTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param big_query_target: big_query_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#big_query_target DataLossPreventionDiscoveryConfig#big_query_target}
        '''
        if isinstance(big_query_target, dict):
            big_query_target = DataLossPreventionDiscoveryConfigTargetsBigQueryTarget(**big_query_target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7e174b998c907bb27da07801d30d0e41c209e0a683353ae0d9eaa66b2e37887)
            check_type(argname="argument big_query_target", value=big_query_target, expected_type=type_hints["big_query_target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if big_query_target is not None:
            self._values["big_query_target"] = big_query_target

    @builtins.property
    def big_query_target(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTarget"]:
        '''big_query_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#big_query_target DataLossPreventionDiscoveryConfig#big_query_target}
        '''
        result = self._values.get("big_query_target")
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTarget"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTarget",
    jsii_struct_bases=[],
    name_mapping={
        "cadence": "cadence",
        "conditions": "conditions",
        "disabled": "disabled",
        "filter": "filter",
    },
)
class DataLossPreventionDiscoveryConfigTargetsBigQueryTarget:
    def __init__(
        self,
        *,
        cadence: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence", typing.Dict[builtins.str, typing.Any]]] = None,
        conditions: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions", typing.Dict[builtins.str, typing.Any]]] = None,
        disabled: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled", typing.Dict[builtins.str, typing.Any]]] = None,
        filter: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cadence: cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#cadence DataLossPreventionDiscoveryConfig#cadence}
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#conditions DataLossPreventionDiscoveryConfig#conditions}
        :param disabled: disabled block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#disabled DataLossPreventionDiscoveryConfig#disabled}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#filter DataLossPreventionDiscoveryConfig#filter}
        '''
        if isinstance(cadence, dict):
            cadence = DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence(**cadence)
        if isinstance(conditions, dict):
            conditions = DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions(**conditions)
        if isinstance(disabled, dict):
            disabled = DataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled(**disabled)
        if isinstance(filter, dict):
            filter = DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter(**filter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c7c0e2c6d70b4a36c43eeb4c0f6a9ea8111a4b835200d9a78eb298b49f48489)
            check_type(argname="argument cadence", value=cadence, expected_type=type_hints["cadence"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cadence is not None:
            self._values["cadence"] = cadence
        if conditions is not None:
            self._values["conditions"] = conditions
        if disabled is not None:
            self._values["disabled"] = disabled
        if filter is not None:
            self._values["filter"] = filter

    @builtins.property
    def cadence(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence"]:
        '''cadence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#cadence DataLossPreventionDiscoveryConfig#cadence}
        '''
        result = self._values.get("cadence")
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence"], result)

    @builtins.property
    def conditions(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions"]:
        '''conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#conditions DataLossPreventionDiscoveryConfig#conditions}
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions"], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled"]:
        '''disabled block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#disabled DataLossPreventionDiscoveryConfig#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled"], result)

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter"]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#filter DataLossPreventionDiscoveryConfig#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigTargetsBigQueryTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence",
    jsii_struct_bases=[],
    name_mapping={
        "schema_modified_cadence": "schemaModifiedCadence",
        "table_modified_cadence": "tableModifiedCadence",
    },
)
class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence:
    def __init__(
        self,
        *,
        schema_modified_cadence: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence", typing.Dict[builtins.str, typing.Any]]] = None,
        table_modified_cadence: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param schema_modified_cadence: schema_modified_cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#schema_modified_cadence DataLossPreventionDiscoveryConfig#schema_modified_cadence}
        :param table_modified_cadence: table_modified_cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#table_modified_cadence DataLossPreventionDiscoveryConfig#table_modified_cadence}
        '''
        if isinstance(schema_modified_cadence, dict):
            schema_modified_cadence = DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence(**schema_modified_cadence)
        if isinstance(table_modified_cadence, dict):
            table_modified_cadence = DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence(**table_modified_cadence)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5b87ddd09bf7d6a496325fcc1700c5b7a2fe841c14e7db4656d827d5b8cfdbc)
            check_type(argname="argument schema_modified_cadence", value=schema_modified_cadence, expected_type=type_hints["schema_modified_cadence"])
            check_type(argname="argument table_modified_cadence", value=table_modified_cadence, expected_type=type_hints["table_modified_cadence"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if schema_modified_cadence is not None:
            self._values["schema_modified_cadence"] = schema_modified_cadence
        if table_modified_cadence is not None:
            self._values["table_modified_cadence"] = table_modified_cadence

    @builtins.property
    def schema_modified_cadence(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence"]:
        '''schema_modified_cadence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#schema_modified_cadence DataLossPreventionDiscoveryConfig#schema_modified_cadence}
        '''
        result = self._values.get("schema_modified_cadence")
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence"], result)

    @builtins.property
    def table_modified_cadence(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence"]:
        '''table_modified_cadence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#table_modified_cadence DataLossPreventionDiscoveryConfig#table_modified_cadence}
        '''
        result = self._values.get("table_modified_cadence")
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63e0abfc09cdb6fc9fbff7faf517a39d36525969421c698aa4989dffb5375681)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSchemaModifiedCadence")
    def put_schema_modified_cadence(
        self,
        *,
        frequency: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param frequency: How frequently profiles may be updated when schemas are modified. Default to monthly Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#frequency DataLossPreventionDiscoveryConfig#frequency}
        :param types: The type of events to consider when deciding if the table's schema has been modified and should have the profile updated. Defaults to NEW_COLUMN. Possible values: ["SCHEMA_NEW_COLUMNS", "SCHEMA_REMOVED_COLUMNS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#types DataLossPreventionDiscoveryConfig#types}
        '''
        value = DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence(
            frequency=frequency, types=types
        )

        return typing.cast(None, jsii.invoke(self, "putSchemaModifiedCadence", [value]))

    @jsii.member(jsii_name="putTableModifiedCadence")
    def put_table_modified_cadence(
        self,
        *,
        frequency: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param frequency: How frequently data profiles can be updated when tables are modified. Defaults to never. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#frequency DataLossPreventionDiscoveryConfig#frequency}
        :param types: The type of events to consider when deciding if the table has been modified and should have the profile updated. Defaults to MODIFIED_TIMESTAMP Possible values: ["TABLE_MODIFIED_TIMESTAMP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#types DataLossPreventionDiscoveryConfig#types}
        '''
        value = DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence(
            frequency=frequency, types=types
        )

        return typing.cast(None, jsii.invoke(self, "putTableModifiedCadence", [value]))

    @jsii.member(jsii_name="resetSchemaModifiedCadence")
    def reset_schema_modified_cadence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaModifiedCadence", []))

    @jsii.member(jsii_name="resetTableModifiedCadence")
    def reset_table_modified_cadence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTableModifiedCadence", []))

    @builtins.property
    @jsii.member(jsii_name="schemaModifiedCadence")
    def schema_modified_cadence(
        self,
    ) -> "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadenceOutputReference":
        return typing.cast("DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadenceOutputReference", jsii.get(self, "schemaModifiedCadence"))

    @builtins.property
    @jsii.member(jsii_name="tableModifiedCadence")
    def table_modified_cadence(
        self,
    ) -> "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadenceOutputReference":
        return typing.cast("DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadenceOutputReference", jsii.get(self, "tableModifiedCadence"))

    @builtins.property
    @jsii.member(jsii_name="schemaModifiedCadenceInput")
    def schema_modified_cadence_input(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence"]:
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence"], jsii.get(self, "schemaModifiedCadenceInput"))

    @builtins.property
    @jsii.member(jsii_name="tableModifiedCadenceInput")
    def table_modified_cadence_input(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence"]:
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence"], jsii.get(self, "tableModifiedCadenceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9777151e6c4a89617dd9181a55b8f7de24a46ff8a87e4f75525e79406ad6e4f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence",
    jsii_struct_bases=[],
    name_mapping={"frequency": "frequency", "types": "types"},
)
class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence:
    def __init__(
        self,
        *,
        frequency: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param frequency: How frequently profiles may be updated when schemas are modified. Default to monthly Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#frequency DataLossPreventionDiscoveryConfig#frequency}
        :param types: The type of events to consider when deciding if the table's schema has been modified and should have the profile updated. Defaults to NEW_COLUMN. Possible values: ["SCHEMA_NEW_COLUMNS", "SCHEMA_REMOVED_COLUMNS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#types DataLossPreventionDiscoveryConfig#types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0b89722136588eb4a1102941a3b0d177d214e601d83726d53120ea1af494a69)
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if frequency is not None:
            self._values["frequency"] = frequency
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def frequency(self) -> typing.Optional[builtins.str]:
        '''How frequently profiles may be updated when schemas are modified. Default to monthly Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#frequency DataLossPreventionDiscoveryConfig#frequency}
        '''
        result = self._values.get("frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The type of events to consider when deciding if the table's schema has been modified and should have the profile updated.

        Defaults to NEW_COLUMN. Possible values: ["SCHEMA_NEW_COLUMNS", "SCHEMA_REMOVED_COLUMNS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#types DataLossPreventionDiscoveryConfig#types}
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadenceOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b431eb34863cf942e5e353d33d999a909e10ea807b4a75578b91b3e9a0769ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFrequency")
    def reset_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrequency", []))

    @jsii.member(jsii_name="resetTypes")
    def reset_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTypes", []))

    @builtins.property
    @jsii.member(jsii_name="frequencyInput")
    def frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="typesInput")
    def types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "typesInput"))

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequency"))

    @frequency.setter
    def frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80bf00056bc50ea90c0a8501271a96e0c5315617f201216bc191696185ebd859)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequency", value)

    @builtins.property
    @jsii.member(jsii_name="types")
    def types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "types"))

    @types.setter
    def types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b6082a86165590583fb063b1fda89b31f0eb7c13cc3fad81e0771addac46e4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "types", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcfe23468024fd1c2c47a97b6f74b510cd2ae7acde8e780da7ffef11381f1146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence",
    jsii_struct_bases=[],
    name_mapping={"frequency": "frequency", "types": "types"},
)
class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence:
    def __init__(
        self,
        *,
        frequency: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param frequency: How frequently data profiles can be updated when tables are modified. Defaults to never. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#frequency DataLossPreventionDiscoveryConfig#frequency}
        :param types: The type of events to consider when deciding if the table has been modified and should have the profile updated. Defaults to MODIFIED_TIMESTAMP Possible values: ["TABLE_MODIFIED_TIMESTAMP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#types DataLossPreventionDiscoveryConfig#types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fa37b8d46ac9453e8c29ac76de2d157b6e136320446266f2163f4d3da8d0b36)
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if frequency is not None:
            self._values["frequency"] = frequency
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def frequency(self) -> typing.Optional[builtins.str]:
        '''How frequently data profiles can be updated when tables are modified. Defaults to never. Possible values: ["UPDATE_FREQUENCY_NEVER", "UPDATE_FREQUENCY_DAILY", "UPDATE_FREQUENCY_MONTHLY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#frequency DataLossPreventionDiscoveryConfig#frequency}
        '''
        result = self._values.get("frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The type of events to consider when deciding if the table has been modified and should have the profile updated.

        Defaults to MODIFIED_TIMESTAMP Possible values: ["TABLE_MODIFIED_TIMESTAMP"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#types DataLossPreventionDiscoveryConfig#types}
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadenceOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b8c71126dff91a658bff9ac432f16af84518a7a37ca282652fc50f0517e706)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFrequency")
    def reset_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrequency", []))

    @jsii.member(jsii_name="resetTypes")
    def reset_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTypes", []))

    @builtins.property
    @jsii.member(jsii_name="frequencyInput")
    def frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="typesInput")
    def types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "typesInput"))

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequency"))

    @frequency.setter
    def frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ea66cf8da41d6f94b19a50a6d3b86056fb2e911a91aed212be8cd9dc5553861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequency", value)

    @builtins.property
    @jsii.member(jsii_name="types")
    def types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "types"))

    @types.setter
    def types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e24bf1c35636fc2f1d5c37936f36898c7a0616a641facaa5c06e317f2bb6fc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "types", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4116c4b7a5a4b217de34a71dcdde6e64c4584b981ceb09e84e3f2c45cb541ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions",
    jsii_struct_bases=[],
    name_mapping={
        "created_after": "createdAfter",
        "or_conditions": "orConditions",
        "type_collection": "typeCollection",
        "types": "types",
    },
)
class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions:
    def __init__(
        self,
        *,
        created_after: typing.Optional[builtins.str] = None,
        or_conditions: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions", typing.Dict[builtins.str, typing.Any]]] = None,
        type_collection: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param created_after: A timestamp in RFC3339 UTC "Zulu" format with nanosecond resolution and upto nine fractional digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#created_after DataLossPreventionDiscoveryConfig#created_after}
        :param or_conditions: or_conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#or_conditions DataLossPreventionDiscoveryConfig#or_conditions}
        :param type_collection: Restrict discovery to categories of table types. Currently view, materialized view, snapshot and non-biglake external tables are supported. Possible values: ["BIG_QUERY_COLLECTION_ALL_TYPES", "BIG_QUERY_COLLECTION_ONLY_SUPPORTED_TYPES"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#type_collection DataLossPreventionDiscoveryConfig#type_collection}
        :param types: types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#types DataLossPreventionDiscoveryConfig#types}
        '''
        if isinstance(or_conditions, dict):
            or_conditions = DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions(**or_conditions)
        if isinstance(types, dict):
            types = DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes(**types)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e40811c9ed72f9cb985943f41662f8d57e8fc1f7b214c0ae742d5621cf6c8ec)
            check_type(argname="argument created_after", value=created_after, expected_type=type_hints["created_after"])
            check_type(argname="argument or_conditions", value=or_conditions, expected_type=type_hints["or_conditions"])
            check_type(argname="argument type_collection", value=type_collection, expected_type=type_hints["type_collection"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if created_after is not None:
            self._values["created_after"] = created_after
        if or_conditions is not None:
            self._values["or_conditions"] = or_conditions
        if type_collection is not None:
            self._values["type_collection"] = type_collection
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def created_after(self) -> typing.Optional[builtins.str]:
        '''A timestamp in RFC3339 UTC "Zulu" format with nanosecond resolution and upto nine fractional digits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#created_after DataLossPreventionDiscoveryConfig#created_after}
        '''
        result = self._values.get("created_after")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def or_conditions(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions"]:
        '''or_conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#or_conditions DataLossPreventionDiscoveryConfig#or_conditions}
        '''
        result = self._values.get("or_conditions")
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions"], result)

    @builtins.property
    def type_collection(self) -> typing.Optional[builtins.str]:
        '''Restrict discovery to categories of table types.

        Currently view, materialized view, snapshot and non-biglake external tables are supported. Possible values: ["BIG_QUERY_COLLECTION_ALL_TYPES", "BIG_QUERY_COLLECTION_ONLY_SUPPORTED_TYPES"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#type_collection DataLossPreventionDiscoveryConfig#type_collection}
        '''
        result = self._values.get("type_collection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def types(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes"]:
        '''types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#types DataLossPreventionDiscoveryConfig#types}
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions",
    jsii_struct_bases=[],
    name_mapping={"min_age": "minAge", "min_row_count": "minRowCount"},
)
class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions:
    def __init__(
        self,
        *,
        min_age: typing.Optional[builtins.str] = None,
        min_row_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param min_age: Duration format. The minimum age a table must have before Cloud DLP can profile it. Value greater than 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#min_age DataLossPreventionDiscoveryConfig#min_age}
        :param min_row_count: Minimum number of rows that should be present before Cloud DLP profiles as a table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#min_row_count DataLossPreventionDiscoveryConfig#min_row_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13358614a41e14878bcd94e19ccdea08a0ceaaf0f120caba92ffd7816b3d8dc5)
            check_type(argname="argument min_age", value=min_age, expected_type=type_hints["min_age"])
            check_type(argname="argument min_row_count", value=min_row_count, expected_type=type_hints["min_row_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if min_age is not None:
            self._values["min_age"] = min_age
        if min_row_count is not None:
            self._values["min_row_count"] = min_row_count

    @builtins.property
    def min_age(self) -> typing.Optional[builtins.str]:
        '''Duration format. The minimum age a table must have before Cloud DLP can profile it. Value greater than 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#min_age DataLossPreventionDiscoveryConfig#min_age}
        '''
        result = self._values.get("min_age")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_row_count(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of rows that should be present before Cloud DLP profiles as a table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#min_row_count DataLossPreventionDiscoveryConfig#min_row_count}
        '''
        result = self._values.get("min_row_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eae8912b758e4aac5f7715afc2bf12e3e5c90381d7ae5116222896db6b53a85)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMinAge")
    def reset_min_age(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinAge", []))

    @jsii.member(jsii_name="resetMinRowCount")
    def reset_min_row_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinRowCount", []))

    @builtins.property
    @jsii.member(jsii_name="minAgeInput")
    def min_age_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minAgeInput"))

    @builtins.property
    @jsii.member(jsii_name="minRowCountInput")
    def min_row_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minRowCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minAge")
    def min_age(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minAge"))

    @min_age.setter
    def min_age(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41731dcb9614a37da4a116011b02712af8a8a924f0762ca4cd37ceb0f2ab4350)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minAge", value)

    @builtins.property
    @jsii.member(jsii_name="minRowCount")
    def min_row_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minRowCount"))

    @min_row_count.setter
    def min_row_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76e6f2f9445f0d92d6fcd16d91c22065e338b6d1611a6a62f3a37f1b2ae13ad7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minRowCount", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6783a90961c6f662ef5b5558e38b0621a8627197a34c240ce9f1bde32e5e776b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff38458495bcd44dd997bed816a78241bfb889df9e85829f3d674a1c18ed4c1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOrConditions")
    def put_or_conditions(
        self,
        *,
        min_age: typing.Optional[builtins.str] = None,
        min_row_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param min_age: Duration format. The minimum age a table must have before Cloud DLP can profile it. Value greater than 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#min_age DataLossPreventionDiscoveryConfig#min_age}
        :param min_row_count: Minimum number of rows that should be present before Cloud DLP profiles as a table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#min_row_count DataLossPreventionDiscoveryConfig#min_row_count}
        '''
        value = DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions(
            min_age=min_age, min_row_count=min_row_count
        )

        return typing.cast(None, jsii.invoke(self, "putOrConditions", [value]))

    @jsii.member(jsii_name="putTypes")
    def put_types(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param types: A set of BiqQuery table types Possible values: ["BIG_QUERY_TABLE_TYPE_TABLE", "BIG_QUERY_TABLE_TYPE_EXTERNAL_BIG_LAKE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#types DataLossPreventionDiscoveryConfig#types}
        '''
        value = DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes(
            types=types
        )

        return typing.cast(None, jsii.invoke(self, "putTypes", [value]))

    @jsii.member(jsii_name="resetCreatedAfter")
    def reset_created_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreatedAfter", []))

    @jsii.member(jsii_name="resetOrConditions")
    def reset_or_conditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrConditions", []))

    @jsii.member(jsii_name="resetTypeCollection")
    def reset_type_collection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTypeCollection", []))

    @jsii.member(jsii_name="resetTypes")
    def reset_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTypes", []))

    @builtins.property
    @jsii.member(jsii_name="orConditions")
    def or_conditions(
        self,
    ) -> DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditionsOutputReference:
        return typing.cast(DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditionsOutputReference, jsii.get(self, "orConditions"))

    @builtins.property
    @jsii.member(jsii_name="types")
    def types(
        self,
    ) -> "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypesOutputReference":
        return typing.cast("DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypesOutputReference", jsii.get(self, "types"))

    @builtins.property
    @jsii.member(jsii_name="createdAfterInput")
    def created_after_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createdAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="orConditionsInput")
    def or_conditions_input(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions], jsii.get(self, "orConditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeCollectionInput")
    def type_collection_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeCollectionInput"))

    @builtins.property
    @jsii.member(jsii_name="typesInput")
    def types_input(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes"]:
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes"], jsii.get(self, "typesInput"))

    @builtins.property
    @jsii.member(jsii_name="createdAfter")
    def created_after(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAfter"))

    @created_after.setter
    def created_after(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff7e27929015c47e4d06ae0540f2af63b22f2be4e0bc5910ce781c75a4a7ec91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createdAfter", value)

    @builtins.property
    @jsii.member(jsii_name="typeCollection")
    def type_collection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "typeCollection"))

    @type_collection.setter
    def type_collection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ecb76eb3f59e8892510cba41f3d2d9b7a35fcce23a4fa86c8aba71fe0d7cea6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "typeCollection", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64a1ce75ba5ae4da1303c3e55c6ddf6e0e3b7c1364c0a2a2e6141f47e1da4bc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param types: A set of BiqQuery table types Possible values: ["BIG_QUERY_TABLE_TYPE_TABLE", "BIG_QUERY_TABLE_TYPE_EXTERNAL_BIG_LAKE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#types DataLossPreventionDiscoveryConfig#types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67280e9bf1d5e889979f0d3e57ab575c176f15bc7f793246dfc7bc3d12a376b6)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of BiqQuery table types Possible values: ["BIG_QUERY_TABLE_TYPE_TABLE", "BIG_QUERY_TABLE_TYPE_EXTERNAL_BIG_LAKE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#types DataLossPreventionDiscoveryConfig#types}
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e34b85252f0449176f471de3c967c2c85240383deb3ba590f8a90ba844be7165)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTypes")
    def reset_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTypes", []))

    @builtins.property
    @jsii.member(jsii_name="typesInput")
    def types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "typesInput"))

    @builtins.property
    @jsii.member(jsii_name="types")
    def types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "types"))

    @types.setter
    def types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__851b627de1c763dcb2ec01568a472cfb37a997b8204fd4460dc5152100150e2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "types", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c6a26f42867f7a74075069260994ffcd01ab2c2e7dec956c763df167197b62a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabledOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabledOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e939fe5ef9a864aeca6a58bfab4aaacf71fc4f196e454a0ee783bf4d0498d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e1bd23fe6bedbe0ae681a16f47609ac37d7dde2a181a79014522639e0d7eb81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter",
    jsii_struct_bases=[],
    name_mapping={"other_tables": "otherTables", "tables": "tables"},
)
class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter:
    def __init__(
        self,
        *,
        other_tables: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables", typing.Dict[builtins.str, typing.Any]]] = None,
        tables: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param other_tables: other_tables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#other_tables DataLossPreventionDiscoveryConfig#other_tables}
        :param tables: tables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#tables DataLossPreventionDiscoveryConfig#tables}
        '''
        if isinstance(other_tables, dict):
            other_tables = DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables(**other_tables)
        if isinstance(tables, dict):
            tables = DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables(**tables)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2a2f362ac51903a83bfe1e00c18069fddba84144a82806ce67bba63fb6e4169)
            check_type(argname="argument other_tables", value=other_tables, expected_type=type_hints["other_tables"])
            check_type(argname="argument tables", value=tables, expected_type=type_hints["tables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if other_tables is not None:
            self._values["other_tables"] = other_tables
        if tables is not None:
            self._values["tables"] = tables

    @builtins.property
    def other_tables(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables"]:
        '''other_tables block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#other_tables DataLossPreventionDiscoveryConfig#other_tables}
        '''
        result = self._values.get("other_tables")
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables"], result)

    @builtins.property
    def tables(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables"]:
        '''tables block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#tables DataLossPreventionDiscoveryConfig#tables}
        '''
        result = self._values.get("tables")
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTablesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTablesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f70d96874687c4efc46f12a0c39d483a97b4848dd1250c0fd133c2264f9a150)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b949c2e0ed34f84d221107948d7c43cf93f7943380ca62f457ccbf4c0865c89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7f178c21a6f31ad17afb94e4661eeea11ec825c46fbc6184d83f733929b7630)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOtherTables")
    def put_other_tables(self) -> None:
        value = DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables()

        return typing.cast(None, jsii.invoke(self, "putOtherTables", [value]))

    @jsii.member(jsii_name="putTables")
    def put_tables(
        self,
        *,
        include_regexes: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param include_regexes: include_regexes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#include_regexes DataLossPreventionDiscoveryConfig#include_regexes}
        '''
        value = DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables(
            include_regexes=include_regexes
        )

        return typing.cast(None, jsii.invoke(self, "putTables", [value]))

    @jsii.member(jsii_name="resetOtherTables")
    def reset_other_tables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOtherTables", []))

    @jsii.member(jsii_name="resetTables")
    def reset_tables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTables", []))

    @builtins.property
    @jsii.member(jsii_name="otherTables")
    def other_tables(
        self,
    ) -> DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTablesOutputReference:
        return typing.cast(DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTablesOutputReference, jsii.get(self, "otherTables"))

    @builtins.property
    @jsii.member(jsii_name="tables")
    def tables(
        self,
    ) -> "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesOutputReference":
        return typing.cast("DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesOutputReference", jsii.get(self, "tables"))

    @builtins.property
    @jsii.member(jsii_name="otherTablesInput")
    def other_tables_input(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables], jsii.get(self, "otherTablesInput"))

    @builtins.property
    @jsii.member(jsii_name="tablesInput")
    def tables_input(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables"]:
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables"], jsii.get(self, "tablesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b946c9948a8ca77f818fcbc9a03439a04dbce5baf2312a1c2c2fa2de03b6403)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables",
    jsii_struct_bases=[],
    name_mapping={"include_regexes": "includeRegexes"},
)
class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables:
    def __init__(
        self,
        *,
        include_regexes: typing.Optional[typing.Union["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param include_regexes: include_regexes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#include_regexes DataLossPreventionDiscoveryConfig#include_regexes}
        '''
        if isinstance(include_regexes, dict):
            include_regexes = DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes(**include_regexes)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f7ab25b771dfebf92bc61da53b9b223c1e176acadd039bbb43f71682230317d)
            check_type(argname="argument include_regexes", value=include_regexes, expected_type=type_hints["include_regexes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if include_regexes is not None:
            self._values["include_regexes"] = include_regexes

    @builtins.property
    def include_regexes(
        self,
    ) -> typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes"]:
        '''include_regexes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#include_regexes DataLossPreventionDiscoveryConfig#include_regexes}
        '''
        result = self._values.get("include_regexes")
        return typing.cast(typing.Optional["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes",
    jsii_struct_bases=[],
    name_mapping={"patterns": "patterns"},
)
class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes:
    def __init__(
        self,
        *,
        patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param patterns: patterns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#patterns DataLossPreventionDiscoveryConfig#patterns}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1c7720d0a5a1501db07cd0b92588d1a57b376993a9191e952399cd8d9f56bd9)
            check_type(argname="argument patterns", value=patterns, expected_type=type_hints["patterns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if patterns is not None:
            self._values["patterns"] = patterns

    @builtins.property
    def patterns(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns"]]]:
        '''patterns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#patterns DataLossPreventionDiscoveryConfig#patterns}
        '''
        result = self._values.get("patterns")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b26a032ca2e2947625c82571b36d1448ef31b61824cbf7ca6352b9be374caf8c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPatterns")
    def put_patterns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5341114e1ec51460c674cb95eb0d10c6ed592a635d0622478dc71eae35575f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPatterns", [value]))

    @jsii.member(jsii_name="resetPatterns")
    def reset_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPatterns", []))

    @builtins.property
    @jsii.member(jsii_name="patterns")
    def patterns(
        self,
    ) -> "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatternsList":
        return typing.cast("DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatternsList", jsii.get(self, "patterns"))

    @builtins.property
    @jsii.member(jsii_name="patternsInput")
    def patterns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns"]]], jsii.get(self, "patternsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__857629c13923e2d0655efe3d457fe5f9f1818c572a908ce2311e20606c049c46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_id_regex": "datasetIdRegex",
        "project_id_regex": "projectIdRegex",
        "table_id_regex": "tableIdRegex",
    },
)
class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns:
    def __init__(
        self,
        *,
        dataset_id_regex: typing.Optional[builtins.str] = None,
        project_id_regex: typing.Optional[builtins.str] = None,
        table_id_regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataset_id_regex: if unset, this property matches all datasets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#dataset_id_regex DataLossPreventionDiscoveryConfig#dataset_id_regex}
        :param project_id_regex: For organizations, if unset, will match all projects. Has no effect for data profile configurations created within a project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#project_id_regex DataLossPreventionDiscoveryConfig#project_id_regex}
        :param table_id_regex: if unset, this property matches all tables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#table_id_regex DataLossPreventionDiscoveryConfig#table_id_regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__954581254e438c78cf19fc23567c6b84e33c07089c931d304d5332860991224a)
            check_type(argname="argument dataset_id_regex", value=dataset_id_regex, expected_type=type_hints["dataset_id_regex"])
            check_type(argname="argument project_id_regex", value=project_id_regex, expected_type=type_hints["project_id_regex"])
            check_type(argname="argument table_id_regex", value=table_id_regex, expected_type=type_hints["table_id_regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dataset_id_regex is not None:
            self._values["dataset_id_regex"] = dataset_id_regex
        if project_id_regex is not None:
            self._values["project_id_regex"] = project_id_regex
        if table_id_regex is not None:
            self._values["table_id_regex"] = table_id_regex

    @builtins.property
    def dataset_id_regex(self) -> typing.Optional[builtins.str]:
        '''if unset, this property matches all datasets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#dataset_id_regex DataLossPreventionDiscoveryConfig#dataset_id_regex}
        '''
        result = self._values.get("dataset_id_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id_regex(self) -> typing.Optional[builtins.str]:
        '''For organizations, if unset, will match all projects. Has no effect for data profile configurations created within a project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#project_id_regex DataLossPreventionDiscoveryConfig#project_id_regex}
        '''
        result = self._values.get("project_id_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_id_regex(self) -> typing.Optional[builtins.str]:
        '''if unset, this property matches all tables.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#table_id_regex DataLossPreventionDiscoveryConfig#table_id_regex}
        '''
        result = self._values.get("table_id_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatternsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatternsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a271872f91c4ebf1b42b30262fdbde34010e27caa898a4c6d575cff6b000a51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatternsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b60ef3aa798a9ffa0fa599ca651f3c7f780d3bf3184c65a5c3685e2e383cda4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatternsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b1aeea78beeb49f0e2a68b329061da36423a1dc3d331f4b1a7eaf1787014f4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11b793a704a3487487de8c002440ba3496dee7386ae676c14a2f04dcbdc1e442)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e8f620bd362d7558e9f4249cf88e497f7fa000a9ddafc54878f9401034c61bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b713195bd7cced33d31bd2743fec9b2cff85da946151395d5f2bd2add77be27a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatternsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatternsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__836b2f4bce39648f36042c02a97106045f1bb184939efd55afd22852d9533d06)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDatasetIdRegex")
    def reset_dataset_id_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatasetIdRegex", []))

    @jsii.member(jsii_name="resetProjectIdRegex")
    def reset_project_id_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectIdRegex", []))

    @jsii.member(jsii_name="resetTableIdRegex")
    def reset_table_id_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTableIdRegex", []))

    @builtins.property
    @jsii.member(jsii_name="datasetIdRegexInput")
    def dataset_id_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdRegexInput")
    def project_id_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="tableIdRegexInput")
    def table_id_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableIdRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetIdRegex")
    def dataset_id_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetIdRegex"))

    @dataset_id_regex.setter
    def dataset_id_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb14ea09d956f4eef243df131896a026698c5568941de9992a7d5d1ec1207146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetIdRegex", value)

    @builtins.property
    @jsii.member(jsii_name="projectIdRegex")
    def project_id_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectIdRegex"))

    @project_id_regex.setter
    def project_id_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe50bcab6fc0f5c4972df63f102feb40fb083b17e73d297e71da3263a5bd269)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectIdRegex", value)

    @builtins.property
    @jsii.member(jsii_name="tableIdRegex")
    def table_id_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableIdRegex"))

    @table_id_regex.setter
    def table_id_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d2bea665e6f18b403f4ffa9de769e2170f25c5ffcbaf2ae7034e429d2ecb2e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableIdRegex", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14519f8f6ff4adf86f597f0dca02150c8e529c257c44067369e9d9de2a74be53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c47ab1b604aa86356aff650c3900a485d477e4540caa52bb8db680245e31abaa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIncludeRegexes")
    def put_include_regexes(
        self,
        *,
        patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param patterns: patterns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#patterns DataLossPreventionDiscoveryConfig#patterns}
        '''
        value = DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes(
            patterns=patterns
        )

        return typing.cast(None, jsii.invoke(self, "putIncludeRegexes", [value]))

    @jsii.member(jsii_name="resetIncludeRegexes")
    def reset_include_regexes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeRegexes", []))

    @builtins.property
    @jsii.member(jsii_name="includeRegexes")
    def include_regexes(
        self,
    ) -> DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesOutputReference:
        return typing.cast(DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesOutputReference, jsii.get(self, "includeRegexes"))

    @builtins.property
    @jsii.member(jsii_name="includeRegexesInput")
    def include_regexes_input(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes], jsii.get(self, "includeRegexesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fe86fa9ee9a5feff084ae735002db326c5709574d5cc77b7da9d1395d50c793)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDiscoveryConfigTargetsBigQueryTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsBigQueryTargetOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffef68e899adcef37b6e2055d292b71a64789fc006e6a8d98e90393775732058)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCadence")
    def put_cadence(
        self,
        *,
        schema_modified_cadence: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence, typing.Dict[builtins.str, typing.Any]]] = None,
        table_modified_cadence: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param schema_modified_cadence: schema_modified_cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#schema_modified_cadence DataLossPreventionDiscoveryConfig#schema_modified_cadence}
        :param table_modified_cadence: table_modified_cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#table_modified_cadence DataLossPreventionDiscoveryConfig#table_modified_cadence}
        '''
        value = DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence(
            schema_modified_cadence=schema_modified_cadence,
            table_modified_cadence=table_modified_cadence,
        )

        return typing.cast(None, jsii.invoke(self, "putCadence", [value]))

    @jsii.member(jsii_name="putConditions")
    def put_conditions(
        self,
        *,
        created_after: typing.Optional[builtins.str] = None,
        or_conditions: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions, typing.Dict[builtins.str, typing.Any]]] = None,
        type_collection: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param created_after: A timestamp in RFC3339 UTC "Zulu" format with nanosecond resolution and upto nine fractional digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#created_after DataLossPreventionDiscoveryConfig#created_after}
        :param or_conditions: or_conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#or_conditions DataLossPreventionDiscoveryConfig#or_conditions}
        :param type_collection: Restrict discovery to categories of table types. Currently view, materialized view, snapshot and non-biglake external tables are supported. Possible values: ["BIG_QUERY_COLLECTION_ALL_TYPES", "BIG_QUERY_COLLECTION_ONLY_SUPPORTED_TYPES"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#type_collection DataLossPreventionDiscoveryConfig#type_collection}
        :param types: types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#types DataLossPreventionDiscoveryConfig#types}
        '''
        value = DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions(
            created_after=created_after,
            or_conditions=or_conditions,
            type_collection=type_collection,
            types=types,
        )

        return typing.cast(None, jsii.invoke(self, "putConditions", [value]))

    @jsii.member(jsii_name="putDisabled")
    def put_disabled(self) -> None:
        value = DataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled()

        return typing.cast(None, jsii.invoke(self, "putDisabled", [value]))

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        *,
        other_tables: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables, typing.Dict[builtins.str, typing.Any]]] = None,
        tables: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param other_tables: other_tables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#other_tables DataLossPreventionDiscoveryConfig#other_tables}
        :param tables: tables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#tables DataLossPreventionDiscoveryConfig#tables}
        '''
        value = DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter(
            other_tables=other_tables, tables=tables
        )

        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="resetCadence")
    def reset_cadence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCadence", []))

    @jsii.member(jsii_name="resetConditions")
    def reset_conditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditions", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @builtins.property
    @jsii.member(jsii_name="cadence")
    def cadence(
        self,
    ) -> DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceOutputReference:
        return typing.cast(DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceOutputReference, jsii.get(self, "cadence"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(
        self,
    ) -> DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOutputReference:
        return typing.cast(DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOutputReference, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(
        self,
    ) -> DataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabledOutputReference:
        return typing.cast(DataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabledOutputReference, jsii.get(self, "disabled"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(
        self,
    ) -> DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOutputReference:
        return typing.cast(DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOutputReference, jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="cadenceInput")
    def cadence_input(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence], jsii.get(self, "cadenceInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionsInput")
    def conditions_input(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions], jsii.get(self, "conditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTarget]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63dc857d0dbbe913a68b4e9a04348b90cc6e04ae1a44f48ec53a898ec32a7625)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDiscoveryConfigTargetsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa15a8c70380d45d3cdce907694c91dc9ec77552f87c926c58bb43da43f90139)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLossPreventionDiscoveryConfigTargetsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e70eb1915660de8034f28b54ac4287e853507756018002f800fc540499cb3f5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLossPreventionDiscoveryConfigTargetsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab20751c52ff10fed8611df881f12828f00c621a646e1d1e5cccc11d758f6d56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d7b4113f9a675047cae09805ca38ef660d560ceef49b56cd6f0faf1d4611563)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__961d99901a595ccd7d4be2d64cd618feed7298fe82bd7f60b09ba2f0b5ee3040)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDiscoveryConfigTargets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDiscoveryConfigTargets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDiscoveryConfigTargets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be1a7c999827d6edd95e141b2edee736bfedb809d66d8f909b0dd1fccb232773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLossPreventionDiscoveryConfigTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTargetsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae738e6062bda83cee40f92e84c8a182cf423ae22e1351aeb20ab2d20d7ecf0b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putBigQueryTarget")
    def put_big_query_target(
        self,
        *,
        cadence: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence, typing.Dict[builtins.str, typing.Any]]] = None,
        conditions: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions, typing.Dict[builtins.str, typing.Any]]] = None,
        disabled: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled, typing.Dict[builtins.str, typing.Any]]] = None,
        filter: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cadence: cadence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#cadence DataLossPreventionDiscoveryConfig#cadence}
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#conditions DataLossPreventionDiscoveryConfig#conditions}
        :param disabled: disabled block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#disabled DataLossPreventionDiscoveryConfig#disabled}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#filter DataLossPreventionDiscoveryConfig#filter}
        '''
        value = DataLossPreventionDiscoveryConfigTargetsBigQueryTarget(
            cadence=cadence, conditions=conditions, disabled=disabled, filter=filter
        )

        return typing.cast(None, jsii.invoke(self, "putBigQueryTarget", [value]))

    @jsii.member(jsii_name="resetBigQueryTarget")
    def reset_big_query_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigQueryTarget", []))

    @builtins.property
    @jsii.member(jsii_name="bigQueryTarget")
    def big_query_target(
        self,
    ) -> DataLossPreventionDiscoveryConfigTargetsBigQueryTargetOutputReference:
        return typing.cast(DataLossPreventionDiscoveryConfigTargetsBigQueryTargetOutputReference, jsii.get(self, "bigQueryTarget"))

    @builtins.property
    @jsii.member(jsii_name="bigQueryTargetInput")
    def big_query_target_input(
        self,
    ) -> typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTarget]:
        return typing.cast(typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTarget], jsii.get(self, "bigQueryTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionDiscoveryConfigTargets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionDiscoveryConfigTargets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionDiscoveryConfigTargets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04fa4cf8d465291d0c03536808a8e6797074ebb601d1f49b991180b043260ec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DataLossPreventionDiscoveryConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#create DataLossPreventionDiscoveryConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#delete DataLossPreventionDiscoveryConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#update DataLossPreventionDiscoveryConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66f4909cfc8391d4d3e14eb61122b07fab84a0c89b31b58aad51f57c60cfcfe7)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#create DataLossPreventionDiscoveryConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#delete DataLossPreventionDiscoveryConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/data_loss_prevention_discovery_config#update DataLossPreventionDiscoveryConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLossPreventionDiscoveryConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLossPreventionDiscoveryConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataLossPreventionDiscoveryConfig.DataLossPreventionDiscoveryConfigTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3300ad3a7cfe5efc678f2800135a57583ca2a4e4e1d82e976486792e5dc9e177)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f98381afcef812ae1ab9f169bf3e27d46c65f645cb9f63e2b73d1cb53d7e4daa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94f0c4e6d9c037901ca1cef81715dea37318ee20aba6e2241c115fab92edd26e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36233d663a69878ab402085dd665bd2a4651e3f3dc826f848e468d39d117d13e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionDiscoveryConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionDiscoveryConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionDiscoveryConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e07fe8089f3356a6ca5283661b270010116df00f8f08d1afa36a09d85fe8d995)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataLossPreventionDiscoveryConfig",
    "DataLossPreventionDiscoveryConfigActions",
    "DataLossPreventionDiscoveryConfigActionsExportData",
    "DataLossPreventionDiscoveryConfigActionsExportDataOutputReference",
    "DataLossPreventionDiscoveryConfigActionsExportDataProfileTable",
    "DataLossPreventionDiscoveryConfigActionsExportDataProfileTableOutputReference",
    "DataLossPreventionDiscoveryConfigActionsList",
    "DataLossPreventionDiscoveryConfigActionsOutputReference",
    "DataLossPreventionDiscoveryConfigActionsPubSubNotification",
    "DataLossPreventionDiscoveryConfigActionsPubSubNotificationOutputReference",
    "DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition",
    "DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions",
    "DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions",
    "DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditionsList",
    "DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditionsOutputReference",
    "DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsOutputReference",
    "DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionOutputReference",
    "DataLossPreventionDiscoveryConfigConfig",
    "DataLossPreventionDiscoveryConfigErrors",
    "DataLossPreventionDiscoveryConfigErrorsDetails",
    "DataLossPreventionDiscoveryConfigErrorsDetailsList",
    "DataLossPreventionDiscoveryConfigErrorsDetailsOutputReference",
    "DataLossPreventionDiscoveryConfigErrorsList",
    "DataLossPreventionDiscoveryConfigErrorsOutputReference",
    "DataLossPreventionDiscoveryConfigOrgConfig",
    "DataLossPreventionDiscoveryConfigOrgConfigLocation",
    "DataLossPreventionDiscoveryConfigOrgConfigLocationOutputReference",
    "DataLossPreventionDiscoveryConfigOrgConfigOutputReference",
    "DataLossPreventionDiscoveryConfigTargets",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTarget",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceOutputReference",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadenceOutputReference",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadenceOutputReference",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditionsOutputReference",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOutputReference",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypesOutputReference",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabledOutputReference",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTablesOutputReference",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOutputReference",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesOutputReference",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatternsList",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatternsOutputReference",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesOutputReference",
    "DataLossPreventionDiscoveryConfigTargetsBigQueryTargetOutputReference",
    "DataLossPreventionDiscoveryConfigTargetsList",
    "DataLossPreventionDiscoveryConfigTargetsOutputReference",
    "DataLossPreventionDiscoveryConfigTimeouts",
    "DataLossPreventionDiscoveryConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__924f5f32f0e280de2745fafbf26e0894a51ebab5e979db1626aa93fb40e973db(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    parent: builtins.str,
    actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDiscoveryConfigActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    inspect_templates: typing.Optional[typing.Sequence[builtins.str]] = None,
    org_config: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigOrgConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    status: typing.Optional[builtins.str] = None,
    targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDiscoveryConfigTargets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3728039a3e9fb7552fe7a7d34a43adeaceeb277b9c34639ea6dede095a2ecd2d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2389950dd6cf60bf989a25578bf22084cb8f61b41e829a0bef177054e5ff0675(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDiscoveryConfigActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e1e013e90c699259a9f67aca7da5239d5a0530bf9428ec62619291dfbb6d5f7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDiscoveryConfigTargets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f41df159678b11c6ebb6c29be22808b75d745e4c9f296b5b612be64896a2eb1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b26a6e8081293d8ff39aca03b13abe4b3bc2bf5b741f8da4155bb03d19235e75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d67cff7986a9a806af85f1407a33812c9f6f5db3289311c3f74a0529516aa28(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52a1431eb31ed73181d36e6e5cccfca570d4b9f614be1255d1d493c46b4a8044(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d57fc28039fa32ba3f027e575bb7a7778c9234638e0542e1f36f5b9f6fccee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70503977e85bce9405e07fd9d51a6a35de34e8e16950d19dfee45f4e9d7819cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abbf47bb422d1bf869b0f79983405cf854e4aec17fb82afad6175df327fe0eb3(
    *,
    export_data: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigActionsExportData, typing.Dict[builtins.str, typing.Any]]] = None,
    pub_sub_notification: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigActionsPubSubNotification, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44c87ac9f2d6015bc04d9029f4cebbdac66e81de8bee4ccdfc31fa118a8efe8c(
    *,
    profile_table: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigActionsExportDataProfileTable, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ebcf4906c00116b97dc8dffc7dda631500b64a496d944e2383dde5b51cdfe78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a85769cd0134c9b9c7e4e7902c758b5b4cc1ccc61d909554359c94e8339e7cb(
    value: typing.Optional[DataLossPreventionDiscoveryConfigActionsExportData],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b491b82e7553868750436b2f05c5396758bb67255a4bf1f4c4f13866ea886d(
    *,
    dataset_id: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
    table_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc5f34b90a3f82e80c47de5455697a035e9ae0859f39022de8bfa2adff03474(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__581c9a28645744cdfd16b58e49bbd338f835e92eff330aa8bcbeacd33184b2a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad7b411ebc23df6d9ebaf68a04c8de4e2e90883674f95cc66ab2dd97a020199c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0930f6d0d54c6fe6726697859dabae0cedd145fc07243d4ed88a29c2b6b6ece7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb6d337100de3ed5c896aba914baf26f9cb7833f3b4c3b8a210c3e093aacbc12(
    value: typing.Optional[DataLossPreventionDiscoveryConfigActionsExportDataProfileTable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__889d51e590628191311c60e9d2b9dc2597af60dc90f9f6a49afaec481be08906(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__562ccde911d8e4f3b485f43463a0cb052ecd996e82fccfa3346e1f145288cf16(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__478c9722145420d26173e94f82f7c8226d2e51711b9ccd1f8e2b66998d4afc6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388063a6904c5e55becd13a666ec6339e1b9e0d9ac94613383fd17ad328c3ec4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b928291d85b3df2052a5b67b92d545dd5ea83093f5797b65079b1e3482b9c442(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f53bfd93997d171f41af215faf10920dbbfa81ff33042f30f83830a382fbd87(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDiscoveryConfigActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acb52dbca95654cdd9b16920290763c8c0a5798ddef2491d7d96215fe063c6ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdadcb3cf5a1adb677ac8d6b6a27040c7c31646d6fe6f0b2188b8f59cad22beb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionDiscoveryConfigActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc76bc5bdd470fec76011737252b713061f6efc2a65798b309e2a7092b944b5a(
    *,
    detail_of_message: typing.Optional[builtins.str] = None,
    event: typing.Optional[builtins.str] = None,
    pubsub_condition: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    topic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__040aa220bf8287cdb5a4edf4cf649331b070d199d1f03583c4e80addc65e11a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7201f77cb19f42683379d00539956b2adc9c1aa25edb9df3f3f7aecbdbe6d2bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f75288df0d650d2e0c8ea1725f0d32e4432a61d9429d4a5290670e9f45d218f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860856839e112139630e606bd01911b571aca115afb2728514929a94f97f3e87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__522c9121a119f67b7d20a9067c679d5b3ea2bab8281678fc8e12fc6495fca66b(
    value: typing.Optional[DataLossPreventionDiscoveryConfigActionsPubSubNotification],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__318e569ab7f37f28fb99d2b6f03e7520ff926ba64827946a4c9a156faf827e43(
    *,
    expressions: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d91930a29ec146016a3307a15037398decbf03a33f022480d6fc36ad2d279213(
    *,
    conditions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    logical_operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3017106ee249b9a7bb2fbf201541b57a5060880f0c3dff0d29eb4be83cef0838(
    *,
    minimum_risk_score: typing.Optional[builtins.str] = None,
    minimum_sensitivity_score: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c5e556cb2478107dce90e6f9fbed84c8c9aef274c8320705f619c46825eff40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__608ad0370b3015495cda3f34c5a991c5ca78339f1f2c268f04167b96a1841d1e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac7215973cca6c562be70df17f179add306f7dd9d86b74911c3b15a158ed4c1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7cee11e11bf6a5ca6e454c8d8f5592c5c75bdfe3e1d5df83c36a98a1504d1be(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce0a6feee4aaa57943d639ffd99645aae4fb7ca1717c0180976e3a6b517c5dcc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3146ac4198c9e0deb2333342c65d6a73675e90037a24d11b5184788d1457993c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ad33fe57fa6b8c99cab2f248e16675b29afad0a9f1ccc8939f6d7954eb254bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f41ace3d0721b70051c6552fa6943b6a094cf62645ee5ae6158eaa5c93fcdffe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856086e455e10c4216aecf6601223ce0801610d0602f774b8e3a2d71b408b234(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3380741e979701127e6656bddef5db508b86150f4e11a22eedfb01165ab59ff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a01c3db3effb217f991b2d1c311f5cc51ab600a9869390f2a93783c9a8baad7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e73ea8ac49b4eef34857d0eca4cf935d18ab70ca11b2facc21b0949165bd6fa7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressionsConditions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2afc2226dafa0b67ff21c6a3a1d59c56a54c05c92cc341526f3dc7b1831bd461(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5430fd65e1a93059a6456ae70dbf2258d9ce62d80e171a27e6894be6d5b59a4(
    value: typing.Optional[DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubConditionExpressions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03d690419caf93a8c62ac0411bf154f1a6192869bd398a422a98292886584d40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60a13a9d02ddb6495b98117d3b5bd7a59f09ed49c78a7c4ecfef6a6e63bcdfb9(
    value: typing.Optional[DataLossPreventionDiscoveryConfigActionsPubSubNotificationPubsubCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e6d090ed62c91d71fb43bb299767dee5f0f87529ceb0e6a0255fc12d82107b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    parent: builtins.str,
    actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDiscoveryConfigActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    inspect_templates: typing.Optional[typing.Sequence[builtins.str]] = None,
    org_config: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigOrgConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    status: typing.Optional[builtins.str] = None,
    targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDiscoveryConfigTargets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55973b60c05c1a8e8744f19cfd627143eb6769e3cc2dcffc43751c49aa8c472b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdebc0d2ec300d7d169bfd455b5cc405a61a894edd0354b6ad4ab177fba18f2d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f462f36128c549d112f0b9723bb9d7d865df8c41710c002e4cb6e80b5d1569f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f8f443c606a04f9de1cbb4f9ae94b00fc89ad2354b78a713d98f87a37d70068(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aebffa7e2ef9faf4a8277cfb517ff48e143367916b79d50bb05fd74464dd18f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef32744ede8fdd27a66957b2aae0c90803540e1abfbbb57b3fb3f7cefa9c1d9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029d17cfecd2b2b6595d229533817faa05d4466a7b7905f416b459d7299f8f8d(
    value: typing.Optional[DataLossPreventionDiscoveryConfigErrorsDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8680e0751404563cc546babe860c24c41a8862a1a2a60f661afe340a3ebfe7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5983ab23aef9842facfbe2b8aefc9d961c7e4685cbea1939ab1383fe782ef36(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7613249358d3a49fb12cd4c9f06cd8e7849639ff34c36bfdd99e3c1b52df4d79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e66bc7d89c9cd027a4347cd5e043feb67be97a7ac8ae1699e08c16f0a353d449(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a549a3f37a98cadbcb674df76e149704b65fe59703943603d80d0502d488a2a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14c3f2dca41b85dad1ac6885a3b0d4cf0855bd7f71248018f851628860ff6ae4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fb8327c35adaba6defd93bdc84816bde7c559bafc3de6fc2c9ef50158e76bd4(
    value: typing.Optional[DataLossPreventionDiscoveryConfigErrors],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5797e1afb754ba6fa0edb772e39d02f5cb4e231af6adc712a13fe7bebcdf049(
    *,
    location: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigOrgConfigLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7770781334409fec5e37cb8eaa71a3ca1cb3dfe04734719b2642ed4e026b43a(
    *,
    folder_id: typing.Optional[builtins.str] = None,
    organization_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad26746672d6f5e1220e87653a91b1c98b51a2a098adae0319f1c185d148b2da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dea563687616e8652054f89c81d4b64fb8715adc16435612cf199b6e40a3f59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43dabdde74b6ba81c8ffec486876826ab588d242f59ae6dab65ba9bec47039b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b3b618189597c00fe40d014a23cd25117e4f266a41c3c502d209cbacad8cc41(
    value: typing.Optional[DataLossPreventionDiscoveryConfigOrgConfigLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b45417518f048225935fe61039200bd76e01ee73caa43cea1ce3d55703fc14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__269718db80ed33aac34de0dfc58893d46b474be380dab1640979b89ddc003082(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df3468ab24efc3720702dc04403f89f028c597d3ae0603a8eadb5ac8435c6877(
    value: typing.Optional[DataLossPreventionDiscoveryConfigOrgConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7e174b998c907bb27da07801d30d0e41c209e0a683353ae0d9eaa66b2e37887(
    *,
    big_query_target: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTarget, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c7c0e2c6d70b4a36c43eeb4c0f6a9ea8111a4b835200d9a78eb298b49f48489(
    *,
    cadence: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence, typing.Dict[builtins.str, typing.Any]]] = None,
    conditions: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions, typing.Dict[builtins.str, typing.Any]]] = None,
    disabled: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled, typing.Dict[builtins.str, typing.Any]]] = None,
    filter: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b87ddd09bf7d6a496325fcc1700c5b7a2fe841c14e7db4656d827d5b8cfdbc(
    *,
    schema_modified_cadence: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence, typing.Dict[builtins.str, typing.Any]]] = None,
    table_modified_cadence: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63e0abfc09cdb6fc9fbff7faf517a39d36525969421c698aa4989dffb5375681(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9777151e6c4a89617dd9181a55b8f7de24a46ff8a87e4f75525e79406ad6e4f0(
    value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0b89722136588eb4a1102941a3b0d177d214e601d83726d53120ea1af494a69(
    *,
    frequency: typing.Optional[builtins.str] = None,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b431eb34863cf942e5e353d33d999a909e10ea807b4a75578b91b3e9a0769ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80bf00056bc50ea90c0a8501271a96e0c5315617f201216bc191696185ebd859(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6082a86165590583fb063b1fda89b31f0eb7c13cc3fad81e0771addac46e4c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcfe23468024fd1c2c47a97b6f74b510cd2ae7acde8e780da7ffef11381f1146(
    value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceSchemaModifiedCadence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa37b8d46ac9453e8c29ac76de2d157b6e136320446266f2163f4d3da8d0b36(
    *,
    frequency: typing.Optional[builtins.str] = None,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b8c71126dff91a658bff9ac432f16af84518a7a37ca282652fc50f0517e706(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea66cf8da41d6f94b19a50a6d3b86056fb2e911a91aed212be8cd9dc5553861(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e24bf1c35636fc2f1d5c37936f36898c7a0616a641facaa5c06e317f2bb6fc8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4116c4b7a5a4b217de34a71dcdde6e64c4584b981ceb09e84e3f2c45cb541ac(
    value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetCadenceTableModifiedCadence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e40811c9ed72f9cb985943f41662f8d57e8fc1f7b214c0ae742d5621cf6c8ec(
    *,
    created_after: typing.Optional[builtins.str] = None,
    or_conditions: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions, typing.Dict[builtins.str, typing.Any]]] = None,
    type_collection: typing.Optional[builtins.str] = None,
    types: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13358614a41e14878bcd94e19ccdea08a0ceaaf0f120caba92ffd7816b3d8dc5(
    *,
    min_age: typing.Optional[builtins.str] = None,
    min_row_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eae8912b758e4aac5f7715afc2bf12e3e5c90381d7ae5116222896db6b53a85(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41731dcb9614a37da4a116011b02712af8a8a924f0762ca4cd37ceb0f2ab4350(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e6f2f9445f0d92d6fcd16d91c22065e338b6d1611a6a62f3a37f1b2ae13ad7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6783a90961c6f662ef5b5558e38b0621a8627197a34c240ce9f1bde32e5e776b(
    value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsOrConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff38458495bcd44dd997bed816a78241bfb889df9e85829f3d674a1c18ed4c1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff7e27929015c47e4d06ae0540f2af63b22f2be4e0bc5910ce781c75a4a7ec91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ecb76eb3f59e8892510cba41f3d2d9b7a35fcce23a4fa86c8aba71fe0d7cea6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a1ce75ba5ae4da1303c3e55c6ddf6e0e3b7c1364c0a2a2e6141f47e1da4bc5(
    value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67280e9bf1d5e889979f0d3e57ab575c176f15bc7f793246dfc7bc3d12a376b6(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34b85252f0449176f471de3c967c2c85240383deb3ba590f8a90ba844be7165(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__851b627de1c763dcb2ec01568a472cfb37a997b8204fd4460dc5152100150e2a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c6a26f42867f7a74075069260994ffcd01ab2c2e7dec956c763df167197b62a(
    value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetConditionsTypes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e939fe5ef9a864aeca6a58bfab4aaacf71fc4f196e454a0ee783bf4d0498d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e1bd23fe6bedbe0ae681a16f47609ac37d7dde2a181a79014522639e0d7eb81(
    value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetDisabled],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2a2f362ac51903a83bfe1e00c18069fddba84144a82806ce67bba63fb6e4169(
    *,
    other_tables: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables, typing.Dict[builtins.str, typing.Any]]] = None,
    tables: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f70d96874687c4efc46f12a0c39d483a97b4848dd1250c0fd133c2264f9a150(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b949c2e0ed34f84d221107948d7c43cf93f7943380ca62f457ccbf4c0865c89(
    value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterOtherTables],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7f178c21a6f31ad17afb94e4661eeea11ec825c46fbc6184d83f733929b7630(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b946c9948a8ca77f818fcbc9a03439a04dbce5baf2312a1c2c2fa2de03b6403(
    value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f7ab25b771dfebf92bc61da53b9b223c1e176acadd039bbb43f71682230317d(
    *,
    include_regexes: typing.Optional[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c7720d0a5a1501db07cd0b92588d1a57b376993a9191e952399cd8d9f56bd9(
    *,
    patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b26a032ca2e2947625c82571b36d1448ef31b61824cbf7ca6352b9be374caf8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5341114e1ec51460c674cb95eb0d10c6ed592a635d0622478dc71eae35575f7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__857629c13923e2d0655efe3d457fe5f9f1818c572a908ce2311e20606c049c46(
    value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__954581254e438c78cf19fc23567c6b84e33c07089c931d304d5332860991224a(
    *,
    dataset_id_regex: typing.Optional[builtins.str] = None,
    project_id_regex: typing.Optional[builtins.str] = None,
    table_id_regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a271872f91c4ebf1b42b30262fdbde34010e27caa898a4c6d575cff6b000a51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b60ef3aa798a9ffa0fa599ca651f3c7f780d3bf3184c65a5c3685e2e383cda4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1aeea78beeb49f0e2a68b329061da36423a1dc3d331f4b1a7eaf1787014f4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11b793a704a3487487de8c002440ba3496dee7386ae676c14a2f04dcbdc1e442(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8f620bd362d7558e9f4249cf88e497f7fa000a9ddafc54878f9401034c61bc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b713195bd7cced33d31bd2743fec9b2cff85da946151395d5f2bd2add77be27a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836b2f4bce39648f36042c02a97106045f1bb184939efd55afd22852d9533d06(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb14ea09d956f4eef243df131896a026698c5568941de9992a7d5d1ec1207146(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe50bcab6fc0f5c4972df63f102feb40fb083b17e73d297e71da3263a5bd269(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d2bea665e6f18b403f4ffa9de769e2170f25c5ffcbaf2ae7034e429d2ecb2e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14519f8f6ff4adf86f597f0dca02150c8e529c257c44067369e9d9de2a74be53(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTablesIncludeRegexesPatterns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c47ab1b604aa86356aff650c3900a485d477e4540caa52bb8db680245e31abaa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fe86fa9ee9a5feff084ae735002db326c5709574d5cc77b7da9d1395d50c793(
    value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTargetFilterTables],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffef68e899adcef37b6e2055d292b71a64789fc006e6a8d98e90393775732058(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63dc857d0dbbe913a68b4e9a04348b90cc6e04ae1a44f48ec53a898ec32a7625(
    value: typing.Optional[DataLossPreventionDiscoveryConfigTargetsBigQueryTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa15a8c70380d45d3cdce907694c91dc9ec77552f87c926c58bb43da43f90139(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e70eb1915660de8034f28b54ac4287e853507756018002f800fc540499cb3f5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab20751c52ff10fed8611df881f12828f00c621a646e1d1e5cccc11d758f6d56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d7b4113f9a675047cae09805ca38ef660d560ceef49b56cd6f0faf1d4611563(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__961d99901a595ccd7d4be2d64cd618feed7298fe82bd7f60b09ba2f0b5ee3040(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1a7c999827d6edd95e141b2edee736bfedb809d66d8f909b0dd1fccb232773(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLossPreventionDiscoveryConfigTargets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae738e6062bda83cee40f92e84c8a182cf423ae22e1351aeb20ab2d20d7ecf0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04fa4cf8d465291d0c03536808a8e6797074ebb601d1f49b991180b043260ec7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionDiscoveryConfigTargets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66f4909cfc8391d4d3e14eb61122b07fab84a0c89b31b58aad51f57c60cfcfe7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3300ad3a7cfe5efc678f2800135a57583ca2a4e4e1d82e976486792e5dc9e177(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f98381afcef812ae1ab9f169bf3e27d46c65f645cb9f63e2b73d1cb53d7e4daa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94f0c4e6d9c037901ca1cef81715dea37318ee20aba6e2241c115fab92edd26e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36233d663a69878ab402085dd665bd2a4651e3f3dc826f848e468d39d117d13e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07fe8089f3356a6ca5283661b270010116df00f8f08d1afa36a09d85fe8d995(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLossPreventionDiscoveryConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
