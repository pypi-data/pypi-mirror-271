# Standard library
import logging

# Third party
import zignal

# Internal
import zoundcard


def play():
    # The recommended way of creating and using a soundcard instance is by using the
    # "with" statement. This will make sure that the instance is closed correctly
    # after usage. See http://effbot.org/zone/python-with-statement.htm
    #
    # This example plays the audio on the default device

    fs = 44100
    x  = zignal.Sinetone(f0=400, fs=fs, duration=1.5, gaindb=-12)
    x2 = zignal.Sinetone(f0=900, fs=fs, duration=1.5, gaindb=-18)

    x.append(x2)
    x.convert_to_float(targetbits=32)

    with zoundcard.PA(device_in='default', device_out='default') as snd:
        snd.play(x)


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
