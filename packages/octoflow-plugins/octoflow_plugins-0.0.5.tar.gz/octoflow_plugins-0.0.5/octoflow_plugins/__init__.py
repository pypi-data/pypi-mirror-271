from octoflow.plugin import Package

__all__ = [
    "package",
]

__version__ = "0.0.5"

package = Package(
    "plugins",
    modules=[
        {
            "name": ".tracking",
            "package": "octoflow_plugins",
        },
    ],
)
