'''
# `google_vertex_ai_dataset`

Refer to the Terraform Registry for docs: [`google_vertex_ai_dataset`](https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset).
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


class VertexAiDataset(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiDataset.VertexAiDataset",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset google_vertex_ai_dataset}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        metadata_schema_uri: builtins.str,
        encryption_spec: typing.Optional[typing.Union["VertexAiDatasetEncryptionSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VertexAiDatasetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset google_vertex_ai_dataset} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: The user-defined name of the Dataset. The name can be up to 128 characters long and can be consist of any UTF-8 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#display_name VertexAiDataset#display_name}
        :param metadata_schema_uri: Points to a YAML file stored on Google Cloud Storage describing additional information about the Dataset. The schema is defined as an OpenAPI 3.0.2 Schema Object. The schema files that can be used here are found in gs://google-cloud-aiplatform/schema/dataset/metadata/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#metadata_schema_uri VertexAiDataset#metadata_schema_uri}
        :param encryption_spec: encryption_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#encryption_spec VertexAiDataset#encryption_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#id VertexAiDataset#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A set of key/value label pairs to assign to this Workflow. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#labels VertexAiDataset#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#project VertexAiDataset#project}.
        :param region: The region of the dataset. eg us-central1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#region VertexAiDataset#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#timeouts VertexAiDataset#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4be10798687ebc0e406b8f297fa093e122713a117e4e0c901461128ad6e2ea12)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VertexAiDatasetConfig(
            display_name=display_name,
            metadata_schema_uri=metadata_schema_uri,
            encryption_spec=encryption_spec,
            id=id,
            labels=labels,
            project=project,
            region=region,
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
        '''Generates CDKTF code for importing a VertexAiDataset resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VertexAiDataset to import.
        :param import_from_id: The id of the existing VertexAiDataset that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VertexAiDataset to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a47fccd2b1e9bf5194230ab9fd19fe376d1dc5bd80ffadb502e22a7b846fc3f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEncryptionSpec")
    def put_encryption_spec(
        self,
        *,
        kms_key_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_name: Required. The Cloud KMS resource identifier of the customer managed encryption key used to protect a resource. Has the form: projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key. The key needs to be in the same region as where the resource is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#kms_key_name VertexAiDataset#kms_key_name}
        '''
        value = VertexAiDatasetEncryptionSpec(kms_key_name=kms_key_name)

        return typing.cast(None, jsii.invoke(self, "putEncryptionSpec", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#create VertexAiDataset#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#delete VertexAiDataset#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#update VertexAiDataset#update}.
        '''
        value = VertexAiDatasetTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetEncryptionSpec")
    def reset_encryption_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionSpec", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="encryptionSpec")
    def encryption_spec(self) -> "VertexAiDatasetEncryptionSpecOutputReference":
        return typing.cast("VertexAiDatasetEncryptionSpecOutputReference", jsii.get(self, "encryptionSpec"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VertexAiDatasetTimeoutsOutputReference":
        return typing.cast("VertexAiDatasetTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionSpecInput")
    def encryption_spec_input(self) -> typing.Optional["VertexAiDatasetEncryptionSpec"]:
        return typing.cast(typing.Optional["VertexAiDatasetEncryptionSpec"], jsii.get(self, "encryptionSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataSchemaUriInput")
    def metadata_schema_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadataSchemaUriInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VertexAiDatasetTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VertexAiDatasetTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d01f380c9f6ccaebabe77f772075da43cd18ce60649ce51eb337fd4b7311f217)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b95c6c0086340dc7b1101bafc444d3827e3dde0abe228381ebfb00ac5b92f2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e33182e1aedc2fb5a241290a650e95e8340441ca16bf04eef2ca0f0dbd5b0989)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="metadataSchemaUri")
    def metadata_schema_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadataSchemaUri"))

    @metadata_schema_uri.setter
    def metadata_schema_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b5f0254a1f3df41d32d6d6e6ba6121f7c201347abfea2abdb04d88fe9829fb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataSchemaUri", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__473e22f91a4bb3d58acf4a345c2563a533603e8d2b5d97399f703e0099aacf40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca6ed2a5b24171f836cdea1e7cf98336e620bdb9eba2667632a5f2bc205eed86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiDataset.VertexAiDatasetConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "display_name": "displayName",
        "metadata_schema_uri": "metadataSchemaUri",
        "encryption_spec": "encryptionSpec",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "region": "region",
        "timeouts": "timeouts",
    },
)
class VertexAiDatasetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        display_name: builtins.str,
        metadata_schema_uri: builtins.str,
        encryption_spec: typing.Optional[typing.Union["VertexAiDatasetEncryptionSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VertexAiDatasetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: The user-defined name of the Dataset. The name can be up to 128 characters long and can be consist of any UTF-8 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#display_name VertexAiDataset#display_name}
        :param metadata_schema_uri: Points to a YAML file stored on Google Cloud Storage describing additional information about the Dataset. The schema is defined as an OpenAPI 3.0.2 Schema Object. The schema files that can be used here are found in gs://google-cloud-aiplatform/schema/dataset/metadata/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#metadata_schema_uri VertexAiDataset#metadata_schema_uri}
        :param encryption_spec: encryption_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#encryption_spec VertexAiDataset#encryption_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#id VertexAiDataset#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A set of key/value label pairs to assign to this Workflow. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#labels VertexAiDataset#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#project VertexAiDataset#project}.
        :param region: The region of the dataset. eg us-central1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#region VertexAiDataset#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#timeouts VertexAiDataset#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(encryption_spec, dict):
            encryption_spec = VertexAiDatasetEncryptionSpec(**encryption_spec)
        if isinstance(timeouts, dict):
            timeouts = VertexAiDatasetTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de286a84d31d195ad2181f53d541b289a0e9259ccef190b08cb063e9bc573788)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument metadata_schema_uri", value=metadata_schema_uri, expected_type=type_hints["metadata_schema_uri"])
            check_type(argname="argument encryption_spec", value=encryption_spec, expected_type=type_hints["encryption_spec"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "metadata_schema_uri": metadata_schema_uri,
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
        if encryption_spec is not None:
            self._values["encryption_spec"] = encryption_spec
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
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
    def display_name(self) -> builtins.str:
        '''The user-defined name of the Dataset.

        The name can be up to 128 characters long and can be consist of any UTF-8 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#display_name VertexAiDataset#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metadata_schema_uri(self) -> builtins.str:
        '''Points to a YAML file stored on Google Cloud Storage describing additional information about the Dataset.

        The schema is defined as an OpenAPI 3.0.2 Schema Object. The schema files that can be used here are found in gs://google-cloud-aiplatform/schema/dataset/metadata/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#metadata_schema_uri VertexAiDataset#metadata_schema_uri}
        '''
        result = self._values.get("metadata_schema_uri")
        assert result is not None, "Required property 'metadata_schema_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_spec(self) -> typing.Optional["VertexAiDatasetEncryptionSpec"]:
        '''encryption_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#encryption_spec VertexAiDataset#encryption_spec}
        '''
        result = self._values.get("encryption_spec")
        return typing.cast(typing.Optional["VertexAiDatasetEncryptionSpec"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#id VertexAiDataset#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value label pairs to assign to this Workflow.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#labels VertexAiDataset#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#project VertexAiDataset#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of the dataset. eg us-central1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#region VertexAiDataset#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VertexAiDatasetTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#timeouts VertexAiDataset#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VertexAiDatasetTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiDatasetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiDataset.VertexAiDatasetEncryptionSpec",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class VertexAiDatasetEncryptionSpec:
    def __init__(self, *, kms_key_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key_name: Required. The Cloud KMS resource identifier of the customer managed encryption key used to protect a resource. Has the form: projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key. The key needs to be in the same region as where the resource is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#kms_key_name VertexAiDataset#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__754bbe806d240481013b67a5f95d440d3c9732b518226193a591ef17b41a7ad5)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''Required.

        The Cloud KMS resource identifier of the customer managed encryption key used to protect a resource.
        Has the form: projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key. The key needs to be in the same region as where the resource is created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#kms_key_name VertexAiDataset#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiDatasetEncryptionSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiDatasetEncryptionSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiDataset.VertexAiDatasetEncryptionSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e0e6ef5d32e65ce2c3cce5d62bac17d31093927f196b643898e6993c5e5a9b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d4c7224d0b8d41b22c281eaf198530f182c361948eac3141f49cadbd80bdc3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VertexAiDatasetEncryptionSpec]:
        return typing.cast(typing.Optional[VertexAiDatasetEncryptionSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiDatasetEncryptionSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14c7a9a6514f3303a9b89d5bc170c12718cea5a50a7d0dec8d1d56826508b86c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiDataset.VertexAiDatasetTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class VertexAiDatasetTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#create VertexAiDataset#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#delete VertexAiDataset#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#update VertexAiDataset#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42c3aa279165a963d1476270cc208f1ec56caa63217eab109691db37e3123258)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#create VertexAiDataset#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#delete VertexAiDataset#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.27.0/docs/resources/vertex_ai_dataset#update VertexAiDataset#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiDatasetTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiDatasetTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiDataset.VertexAiDatasetTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8be6de57aa11803b1ce21f0a295e4fe97cb703e19f42d93cf10d045bd3c8b118)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1f8ce1a6dcda2724b05d0cdbd316f90d0145dc8864a19bfc346c9e4ef84df5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccf335f608cf0f9312ebcd4fbc52c77fa0805da96a8aabe398e642110d7e1c1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__637bb3ea2a65a1ad996fe07af35f9f95ae10a8d6bf43286349f6f62496f95848)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiDatasetTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiDatasetTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiDatasetTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cc4d5c626a7e8a60e0a995422c454c0e1f601767af83909889b984910c64439)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "VertexAiDataset",
    "VertexAiDatasetConfig",
    "VertexAiDatasetEncryptionSpec",
    "VertexAiDatasetEncryptionSpecOutputReference",
    "VertexAiDatasetTimeouts",
    "VertexAiDatasetTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__4be10798687ebc0e406b8f297fa093e122713a117e4e0c901461128ad6e2ea12(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    metadata_schema_uri: builtins.str,
    encryption_spec: typing.Optional[typing.Union[VertexAiDatasetEncryptionSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VertexAiDatasetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2a47fccd2b1e9bf5194230ab9fd19fe376d1dc5bd80ffadb502e22a7b846fc3f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d01f380c9f6ccaebabe77f772075da43cd18ce60649ce51eb337fd4b7311f217(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b95c6c0086340dc7b1101bafc444d3827e3dde0abe228381ebfb00ac5b92f2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e33182e1aedc2fb5a241290a650e95e8340441ca16bf04eef2ca0f0dbd5b0989(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b5f0254a1f3df41d32d6d6e6ba6121f7c201347abfea2abdb04d88fe9829fb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__473e22f91a4bb3d58acf4a345c2563a533603e8d2b5d97399f703e0099aacf40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca6ed2a5b24171f836cdea1e7cf98336e620bdb9eba2667632a5f2bc205eed86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de286a84d31d195ad2181f53d541b289a0e9259ccef190b08cb063e9bc573788(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    metadata_schema_uri: builtins.str,
    encryption_spec: typing.Optional[typing.Union[VertexAiDatasetEncryptionSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VertexAiDatasetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__754bbe806d240481013b67a5f95d440d3c9732b518226193a591ef17b41a7ad5(
    *,
    kms_key_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0e6ef5d32e65ce2c3cce5d62bac17d31093927f196b643898e6993c5e5a9b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d4c7224d0b8d41b22c281eaf198530f182c361948eac3141f49cadbd80bdc3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14c7a9a6514f3303a9b89d5bc170c12718cea5a50a7d0dec8d1d56826508b86c(
    value: typing.Optional[VertexAiDatasetEncryptionSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42c3aa279165a963d1476270cc208f1ec56caa63217eab109691db37e3123258(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8be6de57aa11803b1ce21f0a295e4fe97cb703e19f42d93cf10d045bd3c8b118(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f8ce1a6dcda2724b05d0cdbd316f90d0145dc8864a19bfc346c9e4ef84df5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf335f608cf0f9312ebcd4fbc52c77fa0805da96a8aabe398e642110d7e1c1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__637bb3ea2a65a1ad996fe07af35f9f95ae10a8d6bf43286349f6f62496f95848(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cc4d5c626a7e8a60e0a995422c454c0e1f601767af83909889b984910c64439(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiDatasetTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
