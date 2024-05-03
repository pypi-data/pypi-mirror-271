# HBV-BMI

[![PyPI](https://img.shields.io/pypi/v/HBV)](https://pypi.org/project/HBV/)

Basic Model Interface (BMI) HBV model intended for use with [eWaterCycle](https://github.com/eWaterCycle). See said repo for installation instructions. 

HBV (Hydrologiska Byråns Vattenbalansavdelning) is a conceptual hydrological model. For more information on its history, see this [paper](https://hess.copernicus.org/articles/26/1371/2022/).

_TODO: update to match snow reservoir_

This current implementation is _without_ a snow reservoir, as shown below.
(_Image from the course ENVM1502 - river basin Hydrology (Markus Hrachowitz)._) 
![model_layout.png](https://raw.githubusercontent.com/Daafip/HBV-bmi/main/docs/model_layout.png)

Actual eWatercycle model wrapper can be found on [GitHub](https://github.com/Daafip/ewatercycle-hbv) with accompanying [documentation](https://ewatercycle-hbv.readthedocs.io/en/latest/)

Feel free to fork/duplicate this repo and publish your own (better) version.


## separate use
Can also be used as a standalone package _in theory_ - not advised:

```console
pip install HBV
```

Then HBV becomes available as one of the eWaterCycle models

```python
from HBV import HBV

model = HBV()
```

Be aware of the non-intuitive [BMI](https://github.com/eWaterCycle/grpc4bmi) implementation as this package is designed to run in a [docker](https://github.com/Daafip/HBV-bmi/pkgs/container/hbv-bmi-grpc4bmi) container. 


## Changelog

See [CHANGELOG.md](https://github.com/Daafip/HBV-bmi/blob/main/CHANGELOD.md).