# Peter Hartmeier
# phartmei@uci.edu
# 61283483

import unittest, ds_messenger

class Ds_Mess_Tester(unittest.TestCase):

    def test_send(self):
        print('send')
        dm = ds_messenger.DirectMessenger(username='muah', password='yellow')

        boo = dm.send('hi there to you', 'deboi')

        self.assertEqual(boo, True)

        dm = ds_messenger.DirectMessenger(username='muah', password='yello')

        boo = dm.send('hi there', 'deboi')

        self.assertEqual(boo, False)

    def test_new(self):
        print('new')
        dm = ds_messenger.DirectMessenger(username='muah', password='yellow')
        dm.send('hi there to you', 'deboi')

        dm = ds_messenger.DirectMessenger(username='deboi', password='deboi')

        new = dm.retrieve_new()

        self.assertEqual(type(new), list)
        self.assertEqual(type(new[0]), type(ds_messenger.DirectMessage()))

    def test_all(self):
        print('all')
        dm = ds_messenger.DirectMessenger(username='deboi', password='deboi')

        new = dm.retrieve_new()

        self.assertEqual(type(new), list)
        self.assertEqual(type(new[0]), type(ds_messenger.DirectMessage()))


if __name__ == '__main__':
    if __name__ == '__main__':
        unittest.main()