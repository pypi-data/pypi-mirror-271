# skysurvey-sniapop
extension of skysurvey for snia modelling


# Installation

```bash
git clone https://github.com/MickaelRigault/skysurvey-sniapop.git
cd skysurvey-sniapop
pip install .
```


# basic usage
```python
import skysurvey
import skysurvey_sniapop
brokenalpha_model = skysurvey_sniapop.brokenalpha_model
snia = skysurvey.SNeIa.from_draw(1000, model=brokenalpha_model)
```
