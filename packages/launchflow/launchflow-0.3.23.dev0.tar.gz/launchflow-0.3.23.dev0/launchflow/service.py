from typing import Any, Dict, List, Optional

from launchflow.context import LaunchFlowContext


class Service:

    def __init__(
        self,
        name: str,
        product_name: str,
        create_args: Dict[str, Any],
        dockerfile: str = "Dockerfile",
        build_directory: str = ".",
        build_ignore: List[str] = [],  # type: ignore
    ) -> None:
        self.name = name
        self._product_name = product_name
        self._create_args = create_args
        self._dockerfile = dockerfile
        self._build_directory = build_directory
        self._build_ignore = build_ignore

    def __repr__(self) -> str:
        args = []
        for key, value in self._create_args.items():
            if value is not None:
                args.append(f"{key}={value}")

        base = f"{self.__class__.__name__}(name={self.name}"
        if args:
            base = f"{base}, {', '.join(args)}"
        return base + ")"

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, Service)
            and value.name == self.name
            and value._product_name == self._product_name
            and value._create_args == self._create_args
            and value._dockerfile == self._dockerfile
            and value._build_directory == self._build_directory
            and value._build_ignore == self._build_ignore
        )

    async def deploy_async(
        self,
        *,
        project_name: Optional[str] = None,
        environment_name: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        context = LaunchFlowContext(api_key=api_key)
        return await context.deploy_service_operation_async(
            service_type=self.__class__.__name__,
            product_name=self._product_name,
            create_args=self._create_args,
            dockerfile_path=self._dockerfile,
            build_directory=self._build_directory,
            build_ignore=self._build_ignore,
            service_name=self.name,
            environment_name=environment_name,
            project_name=project_name,
        )

    # TODO: add an sync version of deploy
