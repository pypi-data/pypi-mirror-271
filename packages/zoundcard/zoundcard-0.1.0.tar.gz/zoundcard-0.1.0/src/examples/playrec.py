# Standard library
import logging

# Third party
import zignal

# Internal
import zoundcard


def play_rec():
    # Play and record at the same time

    fs = 44100
    x  = zignal.Sinetone(f0=500, fs=fs, duration=1.5, gaindb=-12)
    x.convert_to_float(targetbits=32)

    with zoundcard.PA(device_in='default', device_out='default') as snd:
        y = snd.play_rec(x, frames_per_buffer=2048)

    y: zignal.Audio
    print(y)
    y.plot()


if __name__ == '__main__':
    logging.basicConfig(
        format="%(levelname)-8s: %(module)s.%(funcName)-15s %(message)s",
        level="DEBUG",
        )
    # some libraries are noisy in DEBUG
    logging.getLogger("matplotlib").setLevel(logging.INFO)
    logging.getLogger("PIL").setLevel(logging.WARNING)

    play_rec()

    print('++ End of script ++')
