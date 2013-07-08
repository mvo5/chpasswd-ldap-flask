import unittest

from mock import (
    patch,
)

import chpasswd_flask


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        chpasswd_flask.app.config['TESTING'] = True
        self.app = chpasswd_flask.app.test_client()

    def test_chpasswd_show(self):
        res = self.app.get("/")
        self.assertTrue("Change password" in res.data)

    def test_chpasswd_change_not_match(self):
        res = self.app.post("/change",
                            data={"user": "user1",
                                  "old_pass": "oldpass",
                                  "new_pass1": "new_pass1",
                                  "new_pass2": "new_pass2",
                                  })
        self.assertEqual(res.data, "passwords don't match")

    @patch("chpasswd_flask.chpasswd_ad")
    def test_chpasswd_change(self, mock_chpasswd):
        res = self.app.post("/change",
                            data={"user": "user1",
                                  "old_pass": "oldpass",
                                  "new_pass1": "new_pass",
                                  "new_pass2": "new_pass",
                                  })
        self.assertEqual(res.data, "Password changed")
        mock_chpasswd.assert_called()


if __name__ == '__main__':
    unittest.main()
