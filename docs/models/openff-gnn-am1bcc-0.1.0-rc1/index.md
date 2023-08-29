# AM1-BCC GNN v0.1.0-rc1

This model is trained to produce AM1-BCC charges similar to OpenEye's implementation.

## Domain

The model is applicable to molecules with:

- elements C, O, H, N, S, F, Br, Cl, I, P
- atoms with between 1 and 6 bonds

It *not* trained on molecules with the following bond patterns:

- `[#15:1]#[*:2]`
- `[#15:1]-[#53:2]`
- `[#15:1]:[*:2]`
- `[#15:1]=[!#6&!#7&!#8&!#16:2]`
- `[#16:1]#[*:2]`
- `[#16:1]-[#35,#53:2]`
- `[#16:1]=[!#15&!#6&!#7&!#8:2]`
- `[#17:1]#,:,=[*:2]`
- `[#17:1]-[!#15&!#16!#6&!#7&!#8:2]`
- `[#1:1]#,:,=[*:2]`
- `[#1:1]-[#1:2]`
- `[#35:1]#,:,=[*:2]`
- `[#35:1]-[!#15&!#6&!#7&!#8:2]`
- `[#53:1]#,:,=[*:2]`
- `[#53:1]-[!#53&!#6&!#7&!#8:2]`
- `[#7:1]#[!#7&!#6:2]`
- `[#8:1]#[*:2]`
- `[#9:1]#,:,=[*:2]`
- `[#9:1]-[!#15&!#16!#6&!#7&!#8:2]`

## Datasets

## Benchmarks

