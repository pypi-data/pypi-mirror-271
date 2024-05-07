from octoflow.plugin import Package

__all__ = [
    "package",
]

package = Package(
    "artifacts",
    modules=[
        {
            "name": ".json_handler",
            "package": "octoflow_plugins.tracking.artifacts",
        },
        {
            "name": ".torch_handler",
            "package": "octoflow_plugins.tracking.artifacts",
        },
        {
            "name": ".pandas_handler",
            "package": "octoflow_plugins.tracking.artifacts",
        },
        {
            "name": ".pickle_handler",
            "package": "octoflow_plugins.tracking.artifacts",
        },
        {
            "name": ".transformers_handler",
            "package": "octoflow_plugins.tracking.artifacts",
        },
    ],
)
