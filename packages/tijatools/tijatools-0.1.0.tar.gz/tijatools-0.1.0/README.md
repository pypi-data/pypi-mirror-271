# tijatools

## Descriptions

The tijatools is a Python package that allows you to display dynamic and customizable progress rings in the terminal. It's an ideal tool for providing visual feedback on the status of long-running operations.

## Installation

```bash
pip install tijatools

## Használat
from tijatools import ProgressRing

# Példányosítsd a ProgressRing osztályt
ring = ProgressRing()

# Indítsd el az animációt
ring.run_with_animation()
