
# Experiments Folder

Here experiments (with algorithms) are placed such as jupyter notebooks.
One can think of them like pages of a lab book.


Naming conv: `exp_[AuthorInitials]_[Order]_[DescriptiveName]`\
example: `exp_PH_001_HowToMultiplyTensors.ipynb`

We want to use literate programming.\
Example of a experiment description:
```python
"""
exp_PH_001_HowToMultiplyTensors.py

The standard order for collapsing indices in tensor multiplication in
deep-learning packages (i.e. batch-first) is inconvenient for inference
during optimization. Quantities like batch-variances can only be
extracted when the order is exchanged.

This experiment shows that the two formulations are in fact equivalent.

Philipp Hennig, April 2014
"""
```
