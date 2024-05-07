import unittest
from unittest.mock import Mock, PropertyMock, patch

from launchflow.aws import RDSPostgres
from launchflow.aws.elasticache import ElasticacheRedis
from launchflow.docker import DockerPostgres, DockerRedis
from launchflow.gcp import CloudSQLPostgres
from launchflow.gcp.memorystore import MemorystoreRedis

import launchflow as lf

IMPORT_BASE = "launchflow.generics"


class GenericPostgresTest(unittest.TestCase):

    def setUp(self) -> None:
        self._config = Mock(spec_set=lf.config)

    def test_local_mode_init(self) -> None:
        with patch(f"{IMPORT_BASE}.launchflow.config.env.local_mode_enabled", new_callable=PropertyMock) as mock_local_mode:
            mock_local_mode.return_value = True
            postgres = lf.Postgres("test-postgres")
            self.assertIsInstance(postgres._strategy, DockerPostgres)

    def test_gcp_mode_init(self) -> None:
        with patch(f"{IMPORT_BASE}.launchflow.config.env", new_callable=PropertyMock) as mock_env:
            mock_env.local_mode_enabled = False
            mock_env.cloud_provider = "gcp"
            postgres = lf.Postgres("test-postgres")

            self.assertIsInstance(postgres._strategy, CloudSQLPostgres)

    def test_awsmode_init(self) -> None:
        with patch(f"{IMPORT_BASE}.launchflow.config.env", new_callable=PropertyMock) as mock_env:
            mock_env.local_mode_enabled = False
            mock_env.cloud_provider = "aws"
            postgres = lf.Postgres("test-postgres")

            self.assertIsInstance(postgres._strategy, RDSPostgres)


class GenericRedisTest(unittest.TestCase):

    def setUp(self) -> None:
        self._config = Mock(spec_set=lf.config)

    def test_local_mode_init(self) -> None:
        with patch(f"{IMPORT_BASE}.launchflow.config.env.local_mode_enabled", new_callable=PropertyMock) as mock_local_mode:
            mock_local_mode.return_value = True
            redis = lf.Redis("test-redis")
            self.assertIsInstance(redis._strategy, DockerRedis)

    def test_gcp_mode_init(self) -> None:
        with patch(f"{IMPORT_BASE}.launchflow.config.env", new_callable=PropertyMock) as mock_env:
            mock_env.local_mode_enabled = False
            mock_env.cloud_provider = "gcp"
            redis = lf.Redis("test-redis")

            self.assertIsInstance(redis._strategy, MemorystoreRedis)

    def test_awsmode_init(self) -> None:
        with patch(f"{IMPORT_BASE}.launchflow.config.env", new_callable=PropertyMock) as mock_env:
            mock_env.local_mode_enabled = False
            mock_env.cloud_provider = "aws"
            redis = lf.Redis("test-redis")

            self.assertIsInstance(redis._strategy, ElasticacheRedis)


if __name__ == "__main__":
    unittest.main()
