# PTCQ
PyTorch Complex Quantization

[![PyPI](https://img.shields.io/pypi/v/ptcq)](https://pypi.org/project/ptcq/)
[![PyPI - License](https://img.shields.io/pypi/l/ptcq)](LICENSE)

> **Note** The quantization is used for result simulation only.
> It is **not** intended for computation acceleration.

## Installation
Install with `pip`:
```
pip install ptcq
```
Install from GitHub Repo:
```
pip install git+https://github.com/Teddy-van-Jerry/ptcq.git
```

## Limitations
PTCQ is actually **fake** quantization that simulates the quantization behavior.
- It does not consider the internal computation quantization process;
- It does not accelerate the computation, still requiring `float` precision;
- Quantization operations have to be implemented manually.

## Implementations

So far, fixed-point quantization for real and complex input has been implemented.
View [API documentation](https://ptcq.tvj.one/en/latest/api/fixed/) for more information.

- `ptcq.FixedQ`: Fixed-point quantization.
- `ptcq.FixedCQ`: Fixed-point complex quantization.

## License
This package is distributed by an [MIT License](LICENSE).
