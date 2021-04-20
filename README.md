# openwebrx-profiles_gen
Generates json with band-profiles (part of config_webrx.py) for OpenWebRX

It's most useful if you want to use OpenWebRX to cover wide spectrum, for example 0MHz-500MHz.  
For public purposes it's reither not recomended to expose more than one band per single SDR device. But if you're the only user, using OpenWebRX alone, you can switch between as many bands as you want!

Note that the result (first of all the `rf_gain`) will likely need to be sometimes adjusted manually for each band separately, with respect to your local conditions (i.e. mostly antenna). What works fine with 80m, whould just fail with 70cm, simple as that.

## Requirements
Fulfilled by the Python Standard Library:
- json
- argparse
- textwrap

## Install
No install method maintained. Download, execute, remove. 
```
git clone git@github.com:SP5D/openwebrx-profiles_gen.git  
cd openwebrx-profiles_gen
python3 openwebrx-profiles_gen.py
```
or
```
curl https://git.io/JOaaS --output openwebrx-profiles_gen.py
python3 openwebrx-profiles_gen.py
```
or   
```
wget https://git.io/JOaaS -O openwebrx-profiles_gen.py  
python3 openwebrx-profiles_gen.py
```

## Usage
```
python3 openwebrx-profiles_gen.py -h
usage: openwebrx-profiles_gen [-h] [-s SAMPLERATE] [-m MOD] [-g RFGAIN] [-o FILE]
                              lowerLimit higherLimit bandwidth

Generates json with band-profiles for OpenWebRX 

positional arguments:
  lowerLimit            The lowest frequency that OpenWebRX will work with.
  higherLimit           The highest frequency that OpenWebRX will work with.
  bandwidth             Width of each generated band profile.

optional arguments:
  -h, --help            show this help message and exit
  -s SAMPLERATE, --samplerate SAMPLERATE
                        Samplerate. Default: 2MHz
  -m MOD, --mod MOD     Start modulation. Default: am
  -g RFGAIN, --rfgain RFGAIN
                        RF gain. Default: auto
  -o FILE, --file FILE  Write result to FILE. If option not provided, result will be
                        printed to stdout.

You can provide each freguency with unit and prefix (for example: 2MHz)
as well as without (example of same value: 2000000).

If (higherLimit-lowerLimit) is not completly divisible by (bandwidth),
the last generated band will be accordingly narrower.
Example:
For lowerLimit 0Hz, higherLimit 10MHz and bandwidth 3MHz,
it will generate bands: 0-3MHz, 3-6MHz, 6-9MHz, 9-10MHz.
```


## Examples
`python3 openwebrx-profiles_gen.py 3.2MHz 14.5MHz 2MHz`  
generates json with profiles from 3.2MHz to 14.5MHz, 2MHz bandwidth:  
```javascript
{
    '3.2-5.2MHz': {
        'name': '3.2-5.2MHz',
        'center_freq': 4200000,
        'rf_gain': 'auto',
        'samp_rate': 2000000,
        'start_freq': 4200000,
        'start_mod': 'am'
    },
    '5.2-7.2MHz': {
        'name': '5.2-7.2MHz',
        'center_freq': 6200000,
        'rf_gain': 'auto',
        'samp_rate': 2000000,
        'start_freq': 6200000,
        'start_mod': 'am'
    },
    '7.2-9.2MHz': {
        'name': '7.2-9.2MHz',
        'center_freq': 8200000,
        'rf_gain': 'auto',
        'samp_rate': 2000000,
        'start_freq': 8200000,
        'start_mod': 'am'
    },
    '9.2-11.2MHz': {
        'name': '9.2-11.2MHz',
        'center_freq': 10200000,
        'rf_gain': 'auto',
        'samp_rate': 2000000,
        'start_freq': 10200000,
        'start_mod': 'am'
    },
    '11.2-13.2MHz': {
        'name': '11.2-13.2MHz',
        'center_freq': 12200000,
        'rf_gain': 'auto',
        'samp_rate': 2000000,
        'start_freq': 12200000,
        'start_mod': 'am'
    },
    '13.2-14.5MHz': {
        'name': '13.2-14.5MHz',
        'center_freq': 13800000,
        'rf_gain': 'auto',
        'samp_rate': 2000000,
        'start_freq': 13800000,
        'start_mod': 'am'
    }
}
```  
