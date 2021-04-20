import json
import argparse
import textwrap


def return_result(result: dict, filename: str):
    if filename:
        file_stream = open(filename, 'a')
        with file_stream as x:
            json.dump(result, x, indent=4)
    else:
        print(result)


# suppress frequencies < 10kHz to 0
# just because 0.009999MHz is as ridiculous as using here scientific notation
# also beautify to int if float fraction is empty
# noinspection PyPep8Naming
def Hz_to_MHz(freq: int):
    prefixed = float(freq / 10 ** 6) if freq >= 10 ** 4 else 0
    return int(prefixed) if int(prefixed) == prefixed else prefixed


# noinspection PyPep8Naming
def any_to_Hz(freq: str):
    if "GHz" in freq:
        return int(float(freq.replace("GHz", "")) * 10 ** 9)
    elif "MHz" in freq:
        return int(float(freq.replace("MHz", "")) * 10 ** 6)
    elif "kHz" in freq:
        return int(float(freq.replace("kHz", "")) * 10 ** 3)
    else:
        return int(freq)


# round nice if possible
# Just visual pedantry, nothing serious
def nice_center_freq(lower: int, higher: int):
    if higher - lower >= 10 ** 6:
        return int((higher + lower) / 2 / 10 ** 5) * 10 ** 5
    elif higher - lower >= 10 ** 3:
        return int((higher + lower) / 2 / 10 ** 2) * 10 ** 2
    else:  # in perfect world this freaking `else` should never happen
        return int((higher + lower) / 2)


def generate_profile(lower: int, higher: int, bandwidth: int,
                     samplerate: int, modulation: str, rfgain: str):
    higher = min(lower + bandwidth, higher)
    return \
        {
            str(Hz_to_MHz(lower)) + "-" +
            str(Hz_to_MHz(higher)) + "MHz":
                {
                    "name":
                        str(Hz_to_MHz(lower)) + "-" +
                        str(Hz_to_MHz(higher)) + "MHz",
                    "center_freq": nice_center_freq(lower, higher),
                    "rf_gain": rfgain,
                    "samp_rate": samplerate,
                    "start_freq": nice_center_freq(lower, higher),
                    "start_mod": modulation
                }
        }


def main(lower_limit: str, higher_limit: str, bandwidth: str,
         samplerate: str, modulation: str, rfgain: str,
         filename: str):
    lower_limit = any_to_Hz(lower_limit)
    higher_limit = any_to_Hz(higher_limit)
    bandwidth = any_to_Hz(bandwidth)
    samplerate = any_to_Hz(samplerate)

    generated_profiles = dict()
    last_highest = lower_limit

    while last_highest < higher_limit:
        generated_profiles.update(
            generate_profile(last_highest, higher_limit, bandwidth,
                             samplerate, modulation, rfgain))
        last_highest += bandwidth

    return_result(generated_profiles, filename)


def cli():
    p = argparse.ArgumentParser(
        prog="openwebrx-profiles_gen",
        description="Generates json with band-profiles for OpenWebRX ",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            '''\
            You can provide each freguency with unit and prefix (for example: 2MHz)
            as well as without (example of same value: 2000000).
        
            If (higherLimit-lowerLimit) is not completly divisible by (bandwidth),
            the last generated band will be accordingly narrower.
            Example:
            For lowerLimit 0Hz, higherLimit 10MHz and bandwidth 3MHz,
            it will generate bands: 0-3MHz, 3-6MHz, 6-9MHz, 9-10MHz.
            '''
        )
    )
    p.add_argument(
        "lowerLimit",
        help="The lowest frequency that OpenWebRX will work with. ",
        type=str
    )
    p.add_argument(
        "higherLimit",
        help="The highest frequency that OpenWebRX will work with. ",
        type=str
    )
    p.add_argument(
        "bandwidth",
        help="Width of each generated band profile. ",
        type=str
    )
    p.add_argument(
        "-s",
        "--samplerate",
        help="Samplerate. Default: 2MHz",
        type=str,
        default="2MHz"
    )
    p.add_argument(
        "-m",
        "--mod",
        help="Start modulation. Default: am",
        type=str,
        default="am"
    )
    p.add_argument(
        "-g",
        "--rfgain",
        help="RF gain. Default: auto",
        type=str,
        default="auto"
    )
    p.add_argument(
        "-o",
        "--file",
        help="Write result to FILE. "
             "If option not provided, result will be printed to stdout.",
        type=str
    )
    args = p.parse_args()

    main(args.lowerLimit, args.higherLimit, args.bandwidth,
         args.samplerate, args.mod, args.rfgain,
         args.file)


if __name__ == '__main__':
    cli()
