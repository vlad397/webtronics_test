import unittest
from task import logs
import io
import sys
from unittest.mock import patch, call

class TestLog(unittest.IsolatedAsyncioTestCase):

    @patch('builtins.print')
    async def test_func(self, mock_print):
        await logs(1, 'name')
        result = ['name', 'line']
        assert mock_print.mock_calls == [call(*result) for _ in range(2)]

if __name__ == '__main__':
    unittest.main()
