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
        self.assertTrue("Change Password" in res.data)

    def test_chpasswd_production_needs_https(self):
        chpasswd_flask.app.config['TESTING'] = False
        res = self.app.get("/")
        self.assertTrue(res.data.endswith("This service needs https\n"))

    def test_chpasswd_change_not_match(self):
        res = self.app.post("/change",
                            data={"user": "user1",
                                  "old_pass": "oldpass",
                                  "new_pass1": "new_pass1",
                                  "new_pass2": "new_pass2",
                                  })
        self.assertEqual(res.data, "passwords don't match")

    def test_chpasswd_change_too_short(self):
        chpasswd_flask.MIN_PASSWORD_SIZE = 8
        res = self.app.post("/change",
                            data={"user": "user1",
                                  "old_pass": "oldpass",
                                  "new_pass1": "1234",
                                  "new_pass2": "1234",
                                  })
        self.assertEqual(res.data, "password too short")

    @patch("chpasswd_flask.chpasswd_ad")
    def test_chpasswd_change(self, mock_chpasswd):
        res = self.app.post("/change",
                            data={"user": "user1",
                                  "old_pass": "oldpass",
                                  "new_pass1": "new_pass123",
                                  "new_pass2": "new_pass123",
                                  })
        self.assertEqual(res.data, "Password changed")
        mock_chpasswd.assert_called_with(
            "ad.example.com", "user1@example.com", "oldpass", "new_pass123")


if __name__ == '__main__':
    unittest.main()
