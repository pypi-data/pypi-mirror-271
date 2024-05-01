'''
# Deploy-time Build

AWS CDK L3 construct that allows you to run a build job for specific purposes. Currently this library supports the following use cases:

* Build web frontend static files
* Build a container image
* Build Seekable OCI (SOCI) indices for container images

## Usage

Install from npm:

```sh
npm i deploy-time-build
```

This library defines several L3 constructs for specific use cases. Here is the usage for each case.

### Build Node.js apps

You can build a Node.js app such as a React frontend app on deploy time by the `NodejsBuild` construct.

![architecture](./imgs/architecture.png)

The following code is an example to use the construct:

```python
import { NodejsBuild } from 'deploy-time-build';

declare const api: apigateway.RestApi;
declare const destinationBucket: s3.IBucket;
declare const distribution: cloudfront.IDistribution;
new NodejsBuild(this, 'ExampleBuild', {
    assets: [
        {
            path: 'example-app',
            exclude: ['dist', 'node_modules'],
        },
    ],
    destinationBucket,
    distribution,
    outputSourceDirectory: 'dist',
    buildCommands: ['npm ci', 'npm run build'],
    buildEnvironment: {
        VITE_API_ENDPOINT: api.url,
    },
});
```

Note that it is possible to pass environment variable `VITE_API_ENDPOINT: api.url` to the construct, which is resolved on deploy time, and injected to the build environment (a vite process in this case.)
The resulting build artifacts will be deployed to `destinationBucket` using a [`s3-deployment.BucketDeployment`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3_deployment.BucketDeployment.html) construct.

You can specify multiple input assets by `assets` property. These assets are extracted to respective sub directories. For example, assume you specified assets like the following:

```python
assets: [
    {
        // directory containing source code and package.json
        path: 'example-app',
        exclude: ['dist', 'node_modules'],
        commands: ['npm install'],
    },
    {
        // directory that is also required for the build
        path: 'module1',
    },
],
```

Then, the extracted directories will be located as the following:

```sh
.                         # a temporary directory (automatically created)
├── example-app           # extracted example-app assets
│   ├── src/              # dist or node_modules directories are excluded even if they exist locally.
│   ├── package.json      # npm install will be executed since its specified in `commands` property.
│   └── package-lock.json
└── module1               # extracted module1 assets
```

You can also override the path where assets are extracted by `extractPath` property for each asset.

With `outputEnvFile` property enabled, a `.env` file is automatically generated and uploaded to your S3 bucket. This file can be used running you frontend project locally. You can download the file to your local machine by running the command added in the stack output.

Please also check [the example directory](./example/) for a complete example.

#### Allowing access from the build environment to other AWS resources

Since `NodejsBuild` construct implements [`iam.IGrantable`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_iam.IGrantable.html) interface, you can use `grant*` method of other constructs to allow access from the build environment.

```python
declare const someBucket: s3.IBucket;
declare const build: NodejsBuild;
someBucket.grantReadWrite(build);
```

You can also use [`iam.Grant`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_iam.Grant.html) class to allow any actions and resources.

```python
declare const build: NodejsBuild;
iam.Grant.addToPrincipal({ grantee: build, actions: ['s3:ListBucket'], resources:['*'] })
```

#### Motivation - why do we need the `NodejsBuild` construct?

I talked about why this construct can be useful in some situations at CDK Day 2023. See the recording or slides below:

[Recording](https://www.youtube.com/live/b-nSH18gFQk?si=ogEZ2x1NixOj6J6j&t=373) | [Slides](https://speakerdeck.com/tmokmss/deploy-web-frontend-apps-with-aws-cdk)

#### Considerations

Since this construct builds your frontend apps every time you deploy the stack and there is any change in input assets (and currently there's even no build cache in the Lambda function!), the time a deployment takes tends to be longer (e.g. a few minutes even for the simple app in `example` directory.) This might results in worse developer experience if you want to deploy changes frequently (imagine `cdk watch` deployment always re-build your frontend app).

To mitigate this issue, you can separate the stack for frontend construct from other stacks especially for a dev environment. Another solution would be to set a fixed string as an asset hash, and avoid builds on every deployment.

```python
      assets: [
        {
          path: '../frontend',
          exclude: ['node_modules', 'dist'],
          commands: ['npm ci'],
          // Set a fixed string as a asset hash to prevent deploying changes.
          // This can be useful for an environment you use to develop locally.
          assetHash: 'frontend_asset',
        },
      ],
```

### Build a container image

You can build a container image at deploy time by the following code:

```python
import { ContainerImageBuild } from 'deploy-time-build';

const image = new ContainerImageBuild(this, 'Build', {
    directory: 'example-image',
    buildArgs: { DUMMY_FILE_SIZE_MB: '15' },
    tag: 'my-image-tag',
});
new DockerImageFunction(this, 'Function', {
    code: image.toLambdaDockerImageCode(),
});
const armImage = new ContainerImageBuild(this, 'BuildArm', {
    directory: 'example-image',
    platform: Platform.LINUX_ARM64,
    repository: image.repository,
    zstdCompression: true,
});
new FargateTaskDefinition(this, 'TaskDefinition', {
    runtimePlatform: { cpuArchitecture: CpuArchitecture.ARM64 }
}).addContainer('main', {
    image: armImage.toEcsDockerImageCode(),
});
```

The third argument (props) are a superset of DockerImageAsset's properties. You can set a few additional properties such as `tag`, `repository`, and `zstdCompression`.

### Build SOCI index for a container image

[Seekable OCI (SOCI)](https://aws.amazon.com/about-aws/whats-new/2022/09/introducing-seekable-oci-lazy-loading-container-images/) is a way to help start tasks faster for Amazon ECS tasks on Fargate 1.4.0. You can build and push a SOCI index using the `SociIndexBuild` construct.

![soci-architecture](imgs/soci-architecture.png)

The following code is an example to use the construct:

```python
import { SociIndexBuild } from 'deploy-time-build';

const asset = new DockerImageAsset(this, 'Image', { directory: 'example-image' });
new SociIndexBuild(this, 'Index', { imageTag: asset.assetHash, repository: asset.repository });
// or using a utility method
SociIndexBuild.fromDockerImageAsset(this, 'Index2', asset);

// Use the asset for ECS Fargate tasks
import { AssetImage } from 'aws-cdk-lib/aws-ecs';
const assetImage = AssetImage.fromDockerImageAsset(asset);
```

We currently use [`soci-wrapper`](https://github.com/tmokmss/soci-wrapper) to build and push SOCI indices.

#### Motivation - why do we need the `SociIndexBuild` construct?

Currently there are several other ways to build a SOCI index; 1. use `soci-snapshotter` CLI, or 2. use [cfn-ecr-aws-soci-index-builder](https://github.com/aws-ia/cfn-ecr-aws-soci-index-builder) solution, none of which can be directly used from AWS CDK. If you are familiar with CDK, you should often deploy container images as CDK assets, which is an ideal way to integrate with other L2 constructs such as ECS. To make the developer experience for SOCI as close as the ordinary container images, the `SociIndexBuild` allows you to deploying a SOCI index directly from CDK, without any dependencies outside of CDK context.

## Development

Commands for maintainers:

```sh
# run test locally
yarn tsc -p tsconfig.dev.json
yarn integ-runner
yarn integ-runner --update-on-failed
```
'''
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

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_cloudfront as _aws_cdk_aws_cloudfront_ceddda9d
import aws_cdk.aws_ecr as _aws_cdk_aws_ecr_ceddda9d
import aws_cdk.aws_ecr_assets as _aws_cdk_aws_ecr_assets_ceddda9d
import aws_cdk.aws_ecs as _aws_cdk_aws_ecs_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_s3_assets as _aws_cdk_aws_s3_assets_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="deploy-time-build.AssetConfig",
    jsii_struct_bases=[_aws_cdk_aws_s3_assets_ceddda9d.AssetProps],
    name_mapping={
        "asset_hash": "assetHash",
        "asset_hash_type": "assetHashType",
        "bundling": "bundling",
        "exclude": "exclude",
        "follow_symlinks": "followSymlinks",
        "ignore_mode": "ignoreMode",
        "readers": "readers",
        "path": "path",
        "commands": "commands",
        "extract_path": "extractPath",
    },
)
class AssetConfig(_aws_cdk_aws_s3_assets_ceddda9d.AssetProps):
    def __init__(
        self,
        *,
        asset_hash: typing.Optional[builtins.str] = None,
        asset_hash_type: typing.Optional[_aws_cdk_ceddda9d.AssetHashType] = None,
        bundling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow_symlinks: typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode] = None,
        ignore_mode: typing.Optional[_aws_cdk_ceddda9d.IgnoreMode] = None,
        readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IGrantable]] = None,
        path: builtins.str,
        commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        extract_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container or a custom bundling provider. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise
        :param exclude: File paths matching the patterns will be excluded. See ``ignoreMode`` to set the matching behavior. Has no effect on Assets bundled using the ``bundling`` property. Default: - nothing is excluded
        :param follow_symlinks: A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        :param ignore_mode: The ignore behavior to use for ``exclude`` patterns. Default: IgnoreMode.GLOB
        :param readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param path: The disk location of the asset. The path should refer to one of the following: - A regular file or a .zip file, in which case the file will be uploaded as-is to S3. - A directory, in which case it will be archived into a .zip file and uploaded to S3.
        :param commands: Shell commands executed right after the asset zip is extracted to the build environment. Default: No command is executed.
        :param extract_path: Relative path from a build directory to the directory where the asset is extracted. Default: basename of the asset path.
        '''
        if isinstance(bundling, dict):
            bundling = _aws_cdk_ceddda9d.BundlingOptions(**bundling)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8e57ab5756054ba32d3c99212a85d1a9c6d99aadd68fa6b763c12872e443675)
            check_type(argname="argument asset_hash", value=asset_hash, expected_type=type_hints["asset_hash"])
            check_type(argname="argument asset_hash_type", value=asset_hash_type, expected_type=type_hints["asset_hash_type"])
            check_type(argname="argument bundling", value=bundling, expected_type=type_hints["bundling"])
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument follow_symlinks", value=follow_symlinks, expected_type=type_hints["follow_symlinks"])
            check_type(argname="argument ignore_mode", value=ignore_mode, expected_type=type_hints["ignore_mode"])
            check_type(argname="argument readers", value=readers, expected_type=type_hints["readers"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument commands", value=commands, expected_type=type_hints["commands"])
            check_type(argname="argument extract_path", value=extract_path, expected_type=type_hints["extract_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }
        if asset_hash is not None:
            self._values["asset_hash"] = asset_hash
        if asset_hash_type is not None:
            self._values["asset_hash_type"] = asset_hash_type
        if bundling is not None:
            self._values["bundling"] = bundling
        if exclude is not None:
            self._values["exclude"] = exclude
        if follow_symlinks is not None:
            self._values["follow_symlinks"] = follow_symlinks
        if ignore_mode is not None:
            self._values["ignore_mode"] = ignore_mode
        if readers is not None:
            self._values["readers"] = readers
        if commands is not None:
            self._values["commands"] = commands
        if extract_path is not None:
            self._values["extract_path"] = extract_path

    @builtins.property
    def asset_hash(self) -> typing.Optional[builtins.str]:
        '''Specify a custom hash for this asset.

        If ``assetHashType`` is set it must
        be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will
        be SHA256 hashed and encoded as hex. The resulting hash will be the asset
        hash.

        NOTE: the hash is used in order to identify a specific revision of the asset, and
        used for optimizing and caching deployment activities related to this asset such as
        packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will
        need to make sure it is updated every time the asset changes, or otherwise it is
        possible that some deployments will not be invalidated.

        :default: - based on ``assetHashType``
        '''
        result = self._values.get("asset_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asset_hash_type(self) -> typing.Optional[_aws_cdk_ceddda9d.AssetHashType]:
        '''Specifies the type of hash to calculate for this asset.

        If ``assetHash`` is configured, this option must be ``undefined`` or
        ``AssetHashType.CUSTOM``.

        :default:

        - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is
        explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        '''
        result = self._values.get("asset_hash_type")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.AssetHashType], result)

    @builtins.property
    def bundling(self) -> typing.Optional[_aws_cdk_ceddda9d.BundlingOptions]:
        '''Bundle the asset by executing a command in a Docker container or a custom bundling provider.

        The asset path will be mounted at ``/asset-input``. The Docker
        container is responsible for putting content at ``/asset-output``.
        The content at ``/asset-output`` will be zipped and used as the
        final asset.

        :default:

        - uploaded as-is to S3 if the asset is a regular file or a .zip file,
        archived into a .zip file and uploaded to S3 otherwise
        '''
        result = self._values.get("bundling")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.BundlingOptions], result)

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''File paths matching the patterns will be excluded.

        See ``ignoreMode`` to set the matching behavior.
        Has no effect on Assets bundled using the ``bundling`` property.

        :default: - nothing is excluded
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def follow_symlinks(self) -> typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode]:
        '''A strategy for how to handle symlinks.

        :default: SymlinkFollowMode.NEVER
        '''
        result = self._values.get("follow_symlinks")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode], result)

    @builtins.property
    def ignore_mode(self) -> typing.Optional[_aws_cdk_ceddda9d.IgnoreMode]:
        '''The ignore behavior to use for ``exclude`` patterns.

        :default: IgnoreMode.GLOB
        '''
        result = self._values.get("ignore_mode")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.IgnoreMode], result)

    @builtins.property
    def readers(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.IGrantable]]:
        '''A list of principals that should be able to read this asset from S3.

        You can use ``asset.grantRead(principal)`` to grant read permissions later.

        :default: - No principals that can read file asset.
        '''
        result = self._values.get("readers")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.IGrantable]], result)

    @builtins.property
    def path(self) -> builtins.str:
        '''The disk location of the asset.

        The path should refer to one of the following:

        - A regular file or a .zip file, in which case the file will be uploaded as-is to S3.
        - A directory, in which case it will be archived into a .zip file and uploaded to S3.
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Shell commands executed right after the asset zip is extracted to the build environment.

        :default: No command is executed.
        '''
        result = self._values.get("commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def extract_path(self) -> typing.Optional[builtins.str]:
        '''Relative path from a build directory to the directory where the asset is extracted.

        :default: basename of the asset path.
        '''
        result = self._values.get("extract_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_iam_ceddda9d.IGrantable)
class ContainerImageBuild(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="deploy-time-build.ContainerImageBuild",
):
    '''Build a container image and push it to an ECR repository on deploy-time.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        repository: typing.Optional[_aws_cdk_aws_ecr_ceddda9d.IRepository] = None,
        tag: typing.Optional[builtins.str] = None,
        zstd_compression: typing.Optional[builtins.bool] = None,
        directory: builtins.str,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file: typing.Optional[builtins.str] = None,
        invalidation: typing.Optional[typing.Union[_aws_cdk_aws_ecr_assets_ceddda9d.DockerImageAssetInvalidationOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        network_mode: typing.Optional[_aws_cdk_aws_ecr_assets_ceddda9d.NetworkMode] = None,
        platform: typing.Optional[_aws_cdk_aws_ecr_assets_ceddda9d.Platform] = None,
        target: typing.Optional[builtins.str] = None,
        extra_hash: typing.Optional[builtins.str] = None,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow_symlinks: typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode] = None,
        ignore_mode: typing.Optional[_aws_cdk_ceddda9d.IgnoreMode] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param repository: The ECR repository to push the image. Default: create a new ECR repository
        :param tag: The tag when to push the image. Default: use assetHash as tag
        :param zstd_compression: Use zstd for compressing a container image. Default: false
        :param directory: The directory where the Dockerfile is stored. Any directory inside with a name that matches the CDK output folder (cdk.out by default) will be excluded from the asset
        :param build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param file: Path to the Dockerfile (relative to the directory). Default: 'Dockerfile'
        :param invalidation: Options to control which parameters are used to invalidate the asset hash. Default: - hash all parameters
        :param network_mode: Networking mode for the RUN commands during build. Support docker API 1.25+. Default: - no networking mode specified (the default networking mode ``NetworkMode.DEFAULT`` will be used)
        :param platform: Platform to build for. *Requires Docker Buildx*. Default: - no platform specified (the current machine architecture will be used)
        :param target: Docker target to build to. Default: - no target
        :param extra_hash: Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param exclude: File paths matching the patterns will be excluded. See ``ignoreMode`` to set the matching behavior. Has no effect on Assets bundled using the ``bundling`` property. Default: - nothing is excluded
        :param follow_symlinks: A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        :param ignore_mode: The ignore behavior to use for ``exclude`` patterns. Default: IgnoreMode.GLOB
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8d9ec5e24290134189760e6d1b810fb7ee3324a2867dc530f78668f65c292d3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ContainerImageBuildProps(
            repository=repository,
            tag=tag,
            zstd_compression=zstd_compression,
            directory=directory,
            build_args=build_args,
            file=file,
            invalidation=invalidation,
            network_mode=network_mode,
            platform=platform,
            target=target,
            extra_hash=extra_hash,
            exclude=exclude,
            follow_symlinks=follow_symlinks,
            ignore_mode=ignore_mode,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="toEcsDockerImageCode")
    def to_ecs_docker_image_code(self) -> _aws_cdk_aws_ecs_ceddda9d.EcrImage:
        '''Get the instance of {@link ContainerImage} for an ECS task definition.'''
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.EcrImage, jsii.invoke(self, "toEcsDockerImageCode", []))

    @jsii.member(jsii_name="toLambdaDockerImageCode")
    def to_lambda_docker_image_code(
        self,
    ) -> _aws_cdk_aws_lambda_ceddda9d.DockerImageCode:
        '''Get the instance of {@link DockerImageCode} for a Lambda function image.'''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.DockerImageCode, jsii.invoke(self, "toLambdaDockerImageCode", []))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''The principal to grant permissions to.'''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageTag"))

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> _aws_cdk_aws_ecr_ceddda9d.IRepository:
        return typing.cast(_aws_cdk_aws_ecr_ceddda9d.IRepository, jsii.get(self, "repository"))


@jsii.data_type(
    jsii_type="deploy-time-build.ContainerImageBuildProps",
    jsii_struct_bases=[_aws_cdk_aws_ecr_assets_ceddda9d.DockerImageAssetProps],
    name_mapping={
        "exclude": "exclude",
        "follow_symlinks": "followSymlinks",
        "ignore_mode": "ignoreMode",
        "extra_hash": "extraHash",
        "build_args": "buildArgs",
        "file": "file",
        "invalidation": "invalidation",
        "network_mode": "networkMode",
        "platform": "platform",
        "target": "target",
        "directory": "directory",
        "repository": "repository",
        "tag": "tag",
        "zstd_compression": "zstdCompression",
    },
)
class ContainerImageBuildProps(_aws_cdk_aws_ecr_assets_ceddda9d.DockerImageAssetProps):
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow_symlinks: typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode] = None,
        ignore_mode: typing.Optional[_aws_cdk_ceddda9d.IgnoreMode] = None,
        extra_hash: typing.Optional[builtins.str] = None,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file: typing.Optional[builtins.str] = None,
        invalidation: typing.Optional[typing.Union[_aws_cdk_aws_ecr_assets_ceddda9d.DockerImageAssetInvalidationOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        network_mode: typing.Optional[_aws_cdk_aws_ecr_assets_ceddda9d.NetworkMode] = None,
        platform: typing.Optional[_aws_cdk_aws_ecr_assets_ceddda9d.Platform] = None,
        target: typing.Optional[builtins.str] = None,
        directory: builtins.str,
        repository: typing.Optional[_aws_cdk_aws_ecr_ceddda9d.IRepository] = None,
        tag: typing.Optional[builtins.str] = None,
        zstd_compression: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param exclude: File paths matching the patterns will be excluded. See ``ignoreMode`` to set the matching behavior. Has no effect on Assets bundled using the ``bundling`` property. Default: - nothing is excluded
        :param follow_symlinks: A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        :param ignore_mode: The ignore behavior to use for ``exclude`` patterns. Default: IgnoreMode.GLOB
        :param extra_hash: Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param file: Path to the Dockerfile (relative to the directory). Default: 'Dockerfile'
        :param invalidation: Options to control which parameters are used to invalidate the asset hash. Default: - hash all parameters
        :param network_mode: Networking mode for the RUN commands during build. Support docker API 1.25+. Default: - no networking mode specified (the default networking mode ``NetworkMode.DEFAULT`` will be used)
        :param platform: Platform to build for. *Requires Docker Buildx*. Default: - no platform specified (the current machine architecture will be used)
        :param target: Docker target to build to. Default: - no target
        :param directory: The directory where the Dockerfile is stored. Any directory inside with a name that matches the CDK output folder (cdk.out by default) will be excluded from the asset
        :param repository: The ECR repository to push the image. Default: create a new ECR repository
        :param tag: The tag when to push the image. Default: use assetHash as tag
        :param zstd_compression: Use zstd for compressing a container image. Default: false
        '''
        if isinstance(invalidation, dict):
            invalidation = _aws_cdk_aws_ecr_assets_ceddda9d.DockerImageAssetInvalidationOptions(**invalidation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04b8bd65bfca7b137073a2a9bdedee6b10ff714618c0018ffcc6ba5061c7bddc)
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument follow_symlinks", value=follow_symlinks, expected_type=type_hints["follow_symlinks"])
            check_type(argname="argument ignore_mode", value=ignore_mode, expected_type=type_hints["ignore_mode"])
            check_type(argname="argument extra_hash", value=extra_hash, expected_type=type_hints["extra_hash"])
            check_type(argname="argument build_args", value=build_args, expected_type=type_hints["build_args"])
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument invalidation", value=invalidation, expected_type=type_hints["invalidation"])
            check_type(argname="argument network_mode", value=network_mode, expected_type=type_hints["network_mode"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument directory", value=directory, expected_type=type_hints["directory"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument zstd_compression", value=zstd_compression, expected_type=type_hints["zstd_compression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "directory": directory,
        }
        if exclude is not None:
            self._values["exclude"] = exclude
        if follow_symlinks is not None:
            self._values["follow_symlinks"] = follow_symlinks
        if ignore_mode is not None:
            self._values["ignore_mode"] = ignore_mode
        if extra_hash is not None:
            self._values["extra_hash"] = extra_hash
        if build_args is not None:
            self._values["build_args"] = build_args
        if file is not None:
            self._values["file"] = file
        if invalidation is not None:
            self._values["invalidation"] = invalidation
        if network_mode is not None:
            self._values["network_mode"] = network_mode
        if platform is not None:
            self._values["platform"] = platform
        if target is not None:
            self._values["target"] = target
        if repository is not None:
            self._values["repository"] = repository
        if tag is not None:
            self._values["tag"] = tag
        if zstd_compression is not None:
            self._values["zstd_compression"] = zstd_compression

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''File paths matching the patterns will be excluded.

        See ``ignoreMode`` to set the matching behavior.
        Has no effect on Assets bundled using the ``bundling`` property.

        :default: - nothing is excluded
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def follow_symlinks(self) -> typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode]:
        '''A strategy for how to handle symlinks.

        :default: SymlinkFollowMode.NEVER
        '''
        result = self._values.get("follow_symlinks")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode], result)

    @builtins.property
    def ignore_mode(self) -> typing.Optional[_aws_cdk_ceddda9d.IgnoreMode]:
        '''The ignore behavior to use for ``exclude`` patterns.

        :default: IgnoreMode.GLOB
        '''
        result = self._values.get("ignore_mode")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.IgnoreMode], result)

    @builtins.property
    def extra_hash(self) -> typing.Optional[builtins.str]:
        '''Extra information to encode into the fingerprint (e.g. build instructions and other inputs).

        :default: - hash is only based on source content
        '''
        result = self._values.get("extra_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Build args to pass to the ``docker build`` command.

        Since Docker build arguments are resolved before deployment, keys and
        values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or
        ``queue.queueUrl``).

        :default: - no build args are passed
        '''
        result = self._values.get("build_args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def file(self) -> typing.Optional[builtins.str]:
        '''Path to the Dockerfile (relative to the directory).

        :default: 'Dockerfile'
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invalidation(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecr_assets_ceddda9d.DockerImageAssetInvalidationOptions]:
        '''Options to control which parameters are used to invalidate the asset hash.

        :default: - hash all parameters
        '''
        result = self._values.get("invalidation")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecr_assets_ceddda9d.DockerImageAssetInvalidationOptions], result)

    @builtins.property
    def network_mode(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecr_assets_ceddda9d.NetworkMode]:
        '''Networking mode for the RUN commands during build.

        Support docker API 1.25+.

        :default: - no networking mode specified (the default networking mode ``NetworkMode.DEFAULT`` will be used)
        '''
        result = self._values.get("network_mode")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecr_assets_ceddda9d.NetworkMode], result)

    @builtins.property
    def platform(self) -> typing.Optional[_aws_cdk_aws_ecr_assets_ceddda9d.Platform]:
        '''Platform to build for.

        *Requires Docker Buildx*.

        :default: - no platform specified (the current machine architecture will be used)
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecr_assets_ceddda9d.Platform], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Docker target to build to.

        :default: - no target
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def directory(self) -> builtins.str:
        '''The directory where the Dockerfile is stored.

        Any directory inside with a name that matches the CDK output folder (cdk.out by default) will be excluded from the asset
        '''
        result = self._values.get("directory")
        assert result is not None, "Required property 'directory' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository(self) -> typing.Optional[_aws_cdk_aws_ecr_ceddda9d.IRepository]:
        '''The ECR repository to push the image.

        :default: create a new ECR repository
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecr_ceddda9d.IRepository], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''The tag when to push the image.

        :default: use assetHash as tag
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zstd_compression(self) -> typing.Optional[builtins.bool]:
        '''Use zstd for compressing a container image.

        :default: false
        '''
        result = self._values.get("zstd_compression")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerImageBuildProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_iam_ceddda9d.IGrantable)
class NodejsBuild(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="deploy-time-build.NodejsBuild",
):
    '''Build Node.js app and optionally publish the artifact to an S3 bucket.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        assets: typing.Sequence[typing.Union[AssetConfig, typing.Dict[builtins.str, typing.Any]]],
        destination_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        output_source_directory: builtins.str,
        build_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        build_environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        destination_key_prefix: typing.Optional[builtins.str] = None,
        distribution: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IDistribution] = None,
        nodejs_version: typing.Optional[jsii.Number] = None,
        output_env_file: typing.Optional[builtins.bool] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param assets: The AssetProps from which s3-assets are created and copied to the build environment.
        :param destination_bucket: S3 Bucket to which your build artifacts are finally deployed.
        :param output_source_directory: Relative path from the working directory to the directory where the build artifacts are output.
        :param build_commands: Shell commands to build your project. They are executed on the working directory you specified. Default: ['npm run build']
        :param build_environment: Environment variables injected to the build environment. You can use CDK deploy-time values as well as literals. Default: {}
        :param destination_key_prefix: Key prefix to deploy your build artifact. Default: '/'
        :param distribution: The distribution you are using to publish you build artifact. If any specified, the caches are invalidated on new artifact deployments. Default: No distribution
        :param nodejs_version: The version of Node.js to use in a build environment. Available versions: 12, 14, 16, 18, 20. Default: 18
        :param output_env_file: If true, a .env file is uploaded to an S3 bucket with values of ``buildEnvironment`` property. You can copy it to your local machine by running the command in the stack output. Default: false
        :param working_directory: Relative path from the build directory to the directory where build commands run. Default: assetProps[0].extractPath
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c71280e3aba0c9512a180cd9b287eb9fa61158e0b247676de51e6b48a0b58d3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NodejsBuildProps(
            assets=assets,
            destination_bucket=destination_bucket,
            output_source_directory=output_source_directory,
            build_commands=build_commands,
            build_environment=build_environment,
            destination_key_prefix=destination_key_prefix,
            distribution=distribution,
            nodejs_version=nodejs_version,
            output_env_file=output_env_file,
            working_directory=working_directory,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''The principal to grant permissions to.'''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.get(self, "grantPrincipal"))


@jsii.data_type(
    jsii_type="deploy-time-build.NodejsBuildProps",
    jsii_struct_bases=[],
    name_mapping={
        "assets": "assets",
        "destination_bucket": "destinationBucket",
        "output_source_directory": "outputSourceDirectory",
        "build_commands": "buildCommands",
        "build_environment": "buildEnvironment",
        "destination_key_prefix": "destinationKeyPrefix",
        "distribution": "distribution",
        "nodejs_version": "nodejsVersion",
        "output_env_file": "outputEnvFile",
        "working_directory": "workingDirectory",
    },
)
class NodejsBuildProps:
    def __init__(
        self,
        *,
        assets: typing.Sequence[typing.Union[AssetConfig, typing.Dict[builtins.str, typing.Any]]],
        destination_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        output_source_directory: builtins.str,
        build_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        build_environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        destination_key_prefix: typing.Optional[builtins.str] = None,
        distribution: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IDistribution] = None,
        nodejs_version: typing.Optional[jsii.Number] = None,
        output_env_file: typing.Optional[builtins.bool] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param assets: The AssetProps from which s3-assets are created and copied to the build environment.
        :param destination_bucket: S3 Bucket to which your build artifacts are finally deployed.
        :param output_source_directory: Relative path from the working directory to the directory where the build artifacts are output.
        :param build_commands: Shell commands to build your project. They are executed on the working directory you specified. Default: ['npm run build']
        :param build_environment: Environment variables injected to the build environment. You can use CDK deploy-time values as well as literals. Default: {}
        :param destination_key_prefix: Key prefix to deploy your build artifact. Default: '/'
        :param distribution: The distribution you are using to publish you build artifact. If any specified, the caches are invalidated on new artifact deployments. Default: No distribution
        :param nodejs_version: The version of Node.js to use in a build environment. Available versions: 12, 14, 16, 18, 20. Default: 18
        :param output_env_file: If true, a .env file is uploaded to an S3 bucket with values of ``buildEnvironment`` property. You can copy it to your local machine by running the command in the stack output. Default: false
        :param working_directory: Relative path from the build directory to the directory where build commands run. Default: assetProps[0].extractPath
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ad4ac39ec4adf96af9bc19519711c6c5d0d566e989bcafec2dac62ce03d3294)
            check_type(argname="argument assets", value=assets, expected_type=type_hints["assets"])
            check_type(argname="argument destination_bucket", value=destination_bucket, expected_type=type_hints["destination_bucket"])
            check_type(argname="argument output_source_directory", value=output_source_directory, expected_type=type_hints["output_source_directory"])
            check_type(argname="argument build_commands", value=build_commands, expected_type=type_hints["build_commands"])
            check_type(argname="argument build_environment", value=build_environment, expected_type=type_hints["build_environment"])
            check_type(argname="argument destination_key_prefix", value=destination_key_prefix, expected_type=type_hints["destination_key_prefix"])
            check_type(argname="argument distribution", value=distribution, expected_type=type_hints["distribution"])
            check_type(argname="argument nodejs_version", value=nodejs_version, expected_type=type_hints["nodejs_version"])
            check_type(argname="argument output_env_file", value=output_env_file, expected_type=type_hints["output_env_file"])
            check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "assets": assets,
            "destination_bucket": destination_bucket,
            "output_source_directory": output_source_directory,
        }
        if build_commands is not None:
            self._values["build_commands"] = build_commands
        if build_environment is not None:
            self._values["build_environment"] = build_environment
        if destination_key_prefix is not None:
            self._values["destination_key_prefix"] = destination_key_prefix
        if distribution is not None:
            self._values["distribution"] = distribution
        if nodejs_version is not None:
            self._values["nodejs_version"] = nodejs_version
        if output_env_file is not None:
            self._values["output_env_file"] = output_env_file
        if working_directory is not None:
            self._values["working_directory"] = working_directory

    @builtins.property
    def assets(self) -> typing.List[AssetConfig]:
        '''The AssetProps from which s3-assets are created and copied to the build environment.'''
        result = self._values.get("assets")
        assert result is not None, "Required property 'assets' is missing"
        return typing.cast(typing.List[AssetConfig], result)

    @builtins.property
    def destination_bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''S3 Bucket to which your build artifacts are finally deployed.'''
        result = self._values.get("destination_bucket")
        assert result is not None, "Required property 'destination_bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    @builtins.property
    def output_source_directory(self) -> builtins.str:
        '''Relative path from the working directory to the directory where the build artifacts are output.'''
        result = self._values.get("output_source_directory")
        assert result is not None, "Required property 'output_source_directory' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def build_commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Shell commands to build your project.

        They are executed on the working directory you specified.

        :default: ['npm run build']
        '''
        result = self._values.get("build_commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def build_environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Environment variables injected to the build environment.

        You can use CDK deploy-time values as well as literals.

        :default: {}
        '''
        result = self._values.get("build_environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def destination_key_prefix(self) -> typing.Optional[builtins.str]:
        '''Key prefix to deploy your build artifact.

        :default: '/'
        '''
        result = self._values.get("destination_key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def distribution(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IDistribution]:
        '''The distribution you are using to publish you build artifact.

        If any specified, the caches are invalidated on new artifact deployments.

        :default: No distribution
        '''
        result = self._values.get("distribution")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IDistribution], result)

    @builtins.property
    def nodejs_version(self) -> typing.Optional[jsii.Number]:
        '''The version of Node.js to use in a build environment. Available versions: 12, 14, 16, 18, 20.

        :default: 18
        '''
        result = self._values.get("nodejs_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def output_env_file(self) -> typing.Optional[builtins.bool]:
        '''If true, a .env file is uploaded to an S3 bucket with values of ``buildEnvironment`` property. You can copy it to your local machine by running the command in the stack output.

        :default: false
        '''
        result = self._values.get("output_env_file")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''Relative path from the build directory to the directory where build commands run.

        :default: assetProps[0].extractPath
        '''
        result = self._values.get("working_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NodejsBuildProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SociIndexBuild(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="deploy-time-build.SociIndexBuild",
):
    '''Build and publish a SOCI index for a container image.

    A SOCI index helps start Fargate tasks faster in some cases.
    Please read the following document for more details: https://docs.aws.amazon.com/AmazonECS/latest/userguide/container-considerations.html
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image_tag: builtins.str,
        repository: _aws_cdk_aws_ecr_ceddda9d.IRepository,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param image_tag: The tag of the container image you want to build index for.
        :param repository: The ECR repository your container image is stored. You can only specify a repository in the same environment (account/region). The index artifact will be uploaded to this repository.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96c9f98c6307010e55fc9821910e21e80021318519921a9cd9371c8e3551dc20)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SociIndexBuildProps(image_tag=image_tag, repository=repository)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromDockerImageAsset")
    @builtins.classmethod
    def from_docker_image_asset(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        image_asset: _aws_cdk_aws_ecr_assets_ceddda9d.DockerImageAsset,
    ) -> "SociIndexBuild":
        '''A utility method to create a SociIndexBuild construct from a DockerImageAsset instance.

        :param scope: -
        :param id: -
        :param image_asset: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__379044f417588697cb394f0bbb2af9baa69f581f01fe14f37a5e9f01ea6c57f3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_asset", value=image_asset, expected_type=type_hints["image_asset"])
        return typing.cast("SociIndexBuild", jsii.sinvoke(cls, "fromDockerImageAsset", [scope, id, image_asset]))


@jsii.data_type(
    jsii_type="deploy-time-build.SociIndexBuildProps",
    jsii_struct_bases=[],
    name_mapping={"image_tag": "imageTag", "repository": "repository"},
)
class SociIndexBuildProps:
    def __init__(
        self,
        *,
        image_tag: builtins.str,
        repository: _aws_cdk_aws_ecr_ceddda9d.IRepository,
    ) -> None:
        '''
        :param image_tag: The tag of the container image you want to build index for.
        :param repository: The ECR repository your container image is stored. You can only specify a repository in the same environment (account/region). The index artifact will be uploaded to this repository.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ad6c57fd92a51686139131b933189975e9f3ea79f0e01e3cdb6be816eed7cb1)
            check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_tag": image_tag,
            "repository": repository,
        }

    @builtins.property
    def image_tag(self) -> builtins.str:
        '''The tag of the container image you want to build index for.'''
        result = self._values.get("image_tag")
        assert result is not None, "Required property 'image_tag' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository(self) -> _aws_cdk_aws_ecr_ceddda9d.IRepository:
        '''The ECR repository your container image is stored.

        You can only specify a repository in the same environment (account/region).
        The index artifact will be uploaded to this repository.
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(_aws_cdk_aws_ecr_ceddda9d.IRepository, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SociIndexBuildProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AssetConfig",
    "ContainerImageBuild",
    "ContainerImageBuildProps",
    "NodejsBuild",
    "NodejsBuildProps",
    "SociIndexBuild",
    "SociIndexBuildProps",
]

publication.publish()

def _typecheckingstub__b8e57ab5756054ba32d3c99212a85d1a9c6d99aadd68fa6b763c12872e443675(
    *,
    asset_hash: typing.Optional[builtins.str] = None,
    asset_hash_type: typing.Optional[_aws_cdk_ceddda9d.AssetHashType] = None,
    bundling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow_symlinks: typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode] = None,
    ignore_mode: typing.Optional[_aws_cdk_ceddda9d.IgnoreMode] = None,
    readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IGrantable]] = None,
    path: builtins.str,
    commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    extract_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d9ec5e24290134189760e6d1b810fb7ee3324a2867dc530f78668f65c292d3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    repository: typing.Optional[_aws_cdk_aws_ecr_ceddda9d.IRepository] = None,
    tag: typing.Optional[builtins.str] = None,
    zstd_compression: typing.Optional[builtins.bool] = None,
    directory: builtins.str,
    build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    file: typing.Optional[builtins.str] = None,
    invalidation: typing.Optional[typing.Union[_aws_cdk_aws_ecr_assets_ceddda9d.DockerImageAssetInvalidationOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    network_mode: typing.Optional[_aws_cdk_aws_ecr_assets_ceddda9d.NetworkMode] = None,
    platform: typing.Optional[_aws_cdk_aws_ecr_assets_ceddda9d.Platform] = None,
    target: typing.Optional[builtins.str] = None,
    extra_hash: typing.Optional[builtins.str] = None,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow_symlinks: typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode] = None,
    ignore_mode: typing.Optional[_aws_cdk_ceddda9d.IgnoreMode] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04b8bd65bfca7b137073a2a9bdedee6b10ff714618c0018ffcc6ba5061c7bddc(
    *,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow_symlinks: typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode] = None,
    ignore_mode: typing.Optional[_aws_cdk_ceddda9d.IgnoreMode] = None,
    extra_hash: typing.Optional[builtins.str] = None,
    build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    file: typing.Optional[builtins.str] = None,
    invalidation: typing.Optional[typing.Union[_aws_cdk_aws_ecr_assets_ceddda9d.DockerImageAssetInvalidationOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    network_mode: typing.Optional[_aws_cdk_aws_ecr_assets_ceddda9d.NetworkMode] = None,
    platform: typing.Optional[_aws_cdk_aws_ecr_assets_ceddda9d.Platform] = None,
    target: typing.Optional[builtins.str] = None,
    directory: builtins.str,
    repository: typing.Optional[_aws_cdk_aws_ecr_ceddda9d.IRepository] = None,
    tag: typing.Optional[builtins.str] = None,
    zstd_compression: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c71280e3aba0c9512a180cd9b287eb9fa61158e0b247676de51e6b48a0b58d3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    assets: typing.Sequence[typing.Union[AssetConfig, typing.Dict[builtins.str, typing.Any]]],
    destination_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    output_source_directory: builtins.str,
    build_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    build_environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    destination_key_prefix: typing.Optional[builtins.str] = None,
    distribution: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IDistribution] = None,
    nodejs_version: typing.Optional[jsii.Number] = None,
    output_env_file: typing.Optional[builtins.bool] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad4ac39ec4adf96af9bc19519711c6c5d0d566e989bcafec2dac62ce03d3294(
    *,
    assets: typing.Sequence[typing.Union[AssetConfig, typing.Dict[builtins.str, typing.Any]]],
    destination_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    output_source_directory: builtins.str,
    build_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    build_environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    destination_key_prefix: typing.Optional[builtins.str] = None,
    distribution: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IDistribution] = None,
    nodejs_version: typing.Optional[jsii.Number] = None,
    output_env_file: typing.Optional[builtins.bool] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c9f98c6307010e55fc9821910e21e80021318519921a9cd9371c8e3551dc20(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image_tag: builtins.str,
    repository: _aws_cdk_aws_ecr_ceddda9d.IRepository,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__379044f417588697cb394f0bbb2af9baa69f581f01fe14f37a5e9f01ea6c57f3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    image_asset: _aws_cdk_aws_ecr_assets_ceddda9d.DockerImageAsset,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad6c57fd92a51686139131b933189975e9f3ea79f0e01e3cdb6be816eed7cb1(
    *,
    image_tag: builtins.str,
    repository: _aws_cdk_aws_ecr_ceddda9d.IRepository,
) -> None:
    """Type checking stubs"""
    pass
