from typing import List

from launchflow.service import Service


class ECSFargate(Service):
    """A service hosted on AWS ECS Fargate.

    ****Example usage:****
    ```python
    import launchflow as lf

    service = lf.aws.ECSFargate("my-service")
    ```

    **NOTE:** This will create the following infrastructure in your AWS account:
    - A [ECS Fargate](https://aws.amazon.com/fargate/) service with the specified configuration.
    - An [Application Load Balancer](https://aws.amazon.com/elasticloadbalancing) to route traffic to the service.
    - A [Code Build](https://aws.amazon.com/codebuild) project that builds and deploys Docker images for the service.
    - An [Elastic Container Registry](https://aws.amazon.com/ecr) repository to store the service's Docker image.
    """

    def __init__(
        self,
        name: str,
        dockerfile: str = "Dockerfile",
        build_directory: str = ".",
        build_ignore: List[str] = [],
    ) -> None:
        """Creates a new ECS Fargate service.

        **Args:**
        - `name`: The name of the service.
        - `build_directory`: The directory to build the service from. This should be a relative path from the project root where your `launchflow.yaml` is defined.
        - `dockerfile`: The Dockerfile to use for building the service. This should be a relative path from the `build_directory`.
        - `build_ignore`: A list of files to ignore when building the service. This can be in the same syntax you would use for a `.gitignore`.
        """
        super().__init__(
            name=name,
            dockerfile=dockerfile,
            product_name="aws_ecs_fargate",
            build_directory=build_directory,
            build_ignore=build_ignore,
            create_args={},
        )
