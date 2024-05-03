import unittest
from unittest.mock import Mock, PropertyMock, patch

from launchflow.aws import RDSPostgres
from launchflow.docker.postgres import DockerPostgres
from launchflow.gcp import CloudSQLPostgres

import launchflow as lf

IMPORT_BASE = "launchflow.postgres"


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


if __name__ == "__main__":
    unittest.main()
