import unittest
from unittest.mock import patch
import os

from services.environment_service import get_env_var

class TestHelpers(unittest.TestCase):

    @patch.dict(os.environ, {'TEST_VAR': 'test_value'})
    def test_get_env_var_success(self):
        # ACT
        result = get_env_var('TEST_VAR')

        # ASSERT
        self.assertEqual(result, 'test_value')

    @patch.dict(os.environ, {}, clear=True)
    def test_get_env_var_not_found(self):
        # ASSIGN
        missing_var = 'MISSING_VAR'

        # ASSERT
        with self.assertRaises(EnvironmentError) as context:
            get_env_var(missing_var)

        self.assertEqual(str(context.exception), f"Environment variable {missing_var} not found.")

if __name__ == '__main__':
    unittest.main()