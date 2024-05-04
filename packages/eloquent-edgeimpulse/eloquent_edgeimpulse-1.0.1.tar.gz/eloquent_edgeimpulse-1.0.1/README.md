# Eloquent EdgeImpulse for Python

A wrapper for Edge Impulse Linux package.

## Setup

To run EI models from Python, you have to deploy a `.eim`
file in the Deployment section by selecting either `Linux` or `macOS`
and make it executable.

Then, install from pip.

```bash
pip install -U eloquent_edgeimpulse
```


## FOMO object detection

To run FOMO, you will need a sample image and a way to load it
(either `PIL` or `scikit-image` or `opencv`)


```python
from PIL import Image
from pprint import pprint
from eloquent_edgeimpulse import Fomo


if __name__ == '__main__':
    fomo = Fomo('./fomo_model.eim')
    image = Image.open('./fomo_sample.jpg').resize(fomo.shape[:2])
    bboxes = fomo.detect(image)
    pprint(bboxes)

>>> [{'cx': 16,
  'cy': 36,
  'height': 8,
  'label': 'leg',
  'score': 0.92578125,
  'value': 0.92578125,
  'width': 16,
  'x': 8,
  'y': 32},
 {'cx': 36,
  'cy': 36,
  'height': 8,
  'label': 'leg',
  'score': 0.9921875,
  'value': 0.9921875,
  'width': 8,
  'x': 32,
  'y': 32}]
```