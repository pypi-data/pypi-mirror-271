# Standard library
import logging
import unittest

# Third party
import zignal

# Internal
import zoundcard


class Test_Stub(unittest.TestCase):
    def setUp(self):
        self.fs = 48000
        self.x = zignal.Sinetones(400, 997, fs=self.fs, duration=2.0)
        self.x.convert_to_float(targetbits=32)

    def test_constructor(self):
        snd = zoundcard.Stub()
        print(snd)
        snd.open()
        snd.close()

    def test_play_open_close(self):
        snd = zoundcard.Stub()
        snd.play(self.x)
        snd.close()

    def test_play(self):
        with zoundcard.Stub() as snd:
            snd.play(self.x)

    def test_rec(self):
        with zoundcard.Stub() as snd:
            y = snd.rec(channels=1, duration=1.0)

        self.assertIsInstance(y, zignal.Audio)

    def test_playrec(self):
        with zoundcard.Stub() as snd:
            y = snd.play_rec(self.x)

        self.assertIsInstance(y, zignal.Audio)
        self.assertEqual(len(self.x), len(y))


if __name__ == "__main__":
    logging.basicConfig(
        format="%(levelname)-8s: %(module)s.%(funcName)-15s %(message)s",
        level="DEBUG",
        )
    # some libraries are noisy in DEBUG
    logging.getLogger("matplotlib").setLevel(logging.INFO)
    logging.getLogger("PIL").setLevel(logging.WARNING)
    logging.getLogger("zignal").setLevel(logging.INFO)

    # from command line:
    # $ python -m unittest -b -v src/tests/test_*.py
    unittest.main(verbosity=2)
