# Peter Hartmeier
# phartmei@uci.edu
# 61283483

import unittest, ds_protocol, time

class Ds_Tester(unittest.TestCase):

    def test_ptp(self):
        x = ds_protocol.ptpsend("Hello World!", "ohhimark", "user_token")

        self.assertEqual(x, '{"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "' + str(time.time()) + '"}}')

    def test_new(self):
        x = ds_protocol.request_new("user_token")

        self.assertEqual(x, '{"token":"user_token", "directmessage": "new"}')

    def test_all(self):
        x = ds_protocol.request_all("user_token")

        self.assertEqual(x, '{"token":"user_token", "directmessage": "all"}')

    def test_dmresponse(self):
        x = ds_protocol.ingest_dmresponse('{"response": {"type": "ok", "message": "Direct message sent"}}')

        self.assertEqual(x, ['ok', "Direct message sent"])
    def test_messresponse(self):
        x = ds_protocol.ingest_messresponse('{"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"}, {"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}]}}')

        self.assertEqual(x, {'markb': [{"message":"Hello User 1!", "timestamp":"1603167689.3928561"}], 'thebeemoviescript': [{"message":"Bzzzzz", "timestamp":"1603167689.3928561"}]})

if __name__ == '__main__':
    if __name__ == '__main__':
        unittest.main()

