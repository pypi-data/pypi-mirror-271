from octoflow.plugin import Package

__all__ = [
    "package",
]

package = Package(
    "tracking",
    modules=[
        {
            "name": ".artifacts",
            "package": "octoflow_plugins.tracking",
        },
    ],
)
