# Standard library
import logging

# Third party
import zignal

# Internal
import zoundcard


def record():
    fs = 44100
    with zoundcard.PA(device_in='default') as snd:
        print("recording...")
        y = snd.rec(duration=3.5, channels=1, fs=fs)

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

    record()

    print('++ End of script ++')
