import unittest

from codechecklib import Tester
from codechecklib.const import ExecStatus


class TestJs(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.tester = Tester()

    async def test_stdin_stdout_ok(self):
        test_program = 'main = putStrLn "Hello, world!"'
        res = await self.tester.run(test_program, 'hs', compilation_max_proc=16)
        print(res.compiler_message)
        self.assertEqual(res.status, ExecStatus.OK)
        self.assertEqual(res.stdout, 'Hello, world!')
        self.assertEqual(res.stderr, '')