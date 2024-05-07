from anyscale._private.sdk import sdk_command
from anyscale.compute_config._private.compute_config_sdk import ComputeConfigSDK
from anyscale.compute_config.models import ComputeConfig


_COMPUTE_CONFIG_SDK_SINGLETON_KEY = "compute_config_sdk"

_CREATE_EXAMPLE = """\
import anyscale
from anyscale.compute_config.models import ComputeConfig, HeadNodeConfig, MarketType, WorkerNodeGroupConfig

config = ComputeConfig(
    head_node=HeadNodeConfig(
        instance_type="m5.8xlarge",
    ),
    worker_nodes=[
        WorkerNodeGroupConfig(
            instance_type="m5.8xlarge",
            min_nodes=5,
            max_nodes=5,
        ),
        WorkerNodeGroupConfig(
            instance_type="m5.4xlarge",
            min_nodes=1,
            max_nodes=10,
            market_type=MarketType.SPOT,
        ),
    ],
)
anyscale.compute_config.create(config, name="my-compute-config")
"""


@sdk_command(
    _COMPUTE_CONFIG_SDK_SINGLETON_KEY,
    ComputeConfigSDK,
    doc_py_example=_CREATE_EXAMPLE,
    arg_docstrings={
        "config": "The config options defining the compute config.",
        "name": "The name of the compute config. This should *not* include a version tag.",
    },
)
def create(config: ComputeConfig, *, name: str, _sdk: ComputeConfigSDK,) -> str:
    """Create a compute config under the specified name.

    Returns the full name of the registered compute config, including the version.
    """
    full_name, _ = _sdk.create_compute_config(config, name=name,)
    return full_name


_GET_EXAMPLE = """\
import anyscale
from anyscale.compute_config.models import ComputeConfig

compute_config: ComputeConfig = anyscale.compute_config.get("my-compute-config")
"""


@sdk_command(
    _COMPUTE_CONFIG_SDK_SINGLETON_KEY,
    ComputeConfigSDK,
    doc_py_example=_GET_EXAMPLE,
    arg_docstrings={
        "name": "The name of the compute config. This can inclue an optional version tag (`<name>:<version>`). If no version tag is provided, the latest version will be returned.",
    },
)
def get(name: str, *, _sdk: ComputeConfigSDK,) -> ComputeConfig:
    """Get the compute config with the specified name.

    The name can contain an optional version, e.g., '<name>:<version>'.
    If no version is provided, the latest one will be returned.
    """
    return _sdk.get_compute_config(name=name)
