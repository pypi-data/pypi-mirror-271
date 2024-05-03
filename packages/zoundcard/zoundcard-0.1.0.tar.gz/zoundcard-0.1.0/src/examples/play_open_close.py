# Standard library
import logging

# Third party
import zignal

# Internal
import zoundcard


def play():
    # Another way of using a soundcard is by first creating an instance and
    # manually calling the open() function. The close() function *must* be
    # called in a controlled fashion. This usually means that the usage is
    # wrapped in a try-except-finally clause.

    fs = 44100
    x  = zignal.Sinetone(f0=700, fs=fs, duration=1.0, gaindb=-24)
    xn = zignal.Noise(channels=1, fs=fs, duration=1.0, gaindb=-12, colour='pink')
    x.append(xn)
    x.convert_to_integer(targetbits=16)

    snd = zoundcard.PA()
    print(snd)

    snd.open()
    try:
        snd.play(x)
    finally:
        snd.close()


if __name__ == '__main__':
    logging.basicConfig(
        format="%(levelname)-8s: %(module)s.%(funcName)-15s %(message)s",
        level="DEBUG",
        )
    # some libraries are noisy in DEBUG
    logging.getLogger("matplotlib").setLevel(logging.INFO)
    logging.getLogger("PIL").setLevel(logging.WARNING)

    play()

    print('++ End of script ++')
