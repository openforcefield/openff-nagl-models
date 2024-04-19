# AM1-BCC GNN v0.1.0-rc2

This model is trained to produce AM1-BCC charges similar to OpenEye's implementation.
It builds off the previously released GNN v0.1.0-rc2 model.

## Training

The model was trained to three targets:

| Target      | Weight | Denominator |
|-------------|--------|-------------|
| Charge RMSE | 1      | 0.02        |
| Dipole RMSE | 1      | 0.1         |
| Weighted ESP RMSE    | 1      | 0.001       |


## Domain

The model is applicable to molecules with:

- elements C, O, H, N, S, F, Br, Cl, I, P
- atoms with between 1 and 6 bonds

It is *not* trained on molecules with the following bond patterns:

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

### Sources

This model was trained, validated, and tested on the following datasets:

|                                          | Training | Validation | Test  | Source                                                      |
|------------------------------------------|----------|------------|-------|-------------------------------------------------------------|
| Enamine Discovery Diversity Set (DDS-10) | 6499     | 2524       |       | [Enamine DDS-10][enamine-10240]                             |
| Enamine Discovery Diversity Set (DDS-50) | 35731    | 8072       |       | [Enamine DDS-50][enamine-50240]                             |
| Diverse ChEMBL training molecules        | 31185    | 8564       |       | [Bleiziffer, Schaller, and  Riniker, 2018][riniker]         |
| Diverse ZINC training molecules          | 78933    | 15267      |       | [Bleiziffer, Schaller, and  Riniker, 2018][riniker]         |
| NCI 250K                                 | 85322    | 22513      |       | [Release 4 File Series - May 2012][nci-250k]                |
| PDB                                      | 10844    | 4653       |       | [Ligand Expo][pdb]                                          |
| Peptides (1-4 AA)                        | 22690    |            |       | Generated from RDKit through combinations of FASTA codes    |
| Small ChEMBL molecules   (< 200 Da)      | 39909    |            | 17104 | Curated from the [ChEMBL][ChEMBL] database.                 |
| OpenFF Industry Benchmark Set (v1.1)     |          |            | 13671 | [QCArchive Submission][qca-openff-benchmark]                |
| SPICE                                    |          |            | 14652 | [SPICE dataset][spice]                                      |
| Peptides with PTMs                       |          |            | 6073  | Peptide chains with common post-translational modifications |
| Total                                    | 271204   | 61593      | 34396 |                                                             |


[enamine-10240]: https://enamine.net/compound-libraries/diversity-libraries/dds-10560
[enamine-50240]: https://enamine.net/compound-libraries/diversity-libraries/dds-50240
[riniker]: https://doi.org/10.1021/acs.jcim.7b00663
[nci-250k]: https://cactus.nci.nih.gov/download/nci/
[pdb]: http://ligand-expo.rcsb.org/dictionaries/Components-smiles-stereo-oe.smi
[qca-openff-benchmark]: https://github.com/openforcefield/qca-dataset-submission/tree/master/submissions/2021-06-04-OpenFF-Industry-Benchmark-Season-1-v1.1
[spice]: https://doi.org/10.1038/s41597-022-01882-6
[ChEMBL]: https://www.ebi.ac.uk/chembl/

### Characterisation

#### Elements

| Element | Training | Validation | Test  |
|---------|----------|------------|-------|
| H       | 310828   | 61582      | 52820 |
| C       | 311043   | 61592      | 52968 |
| N       | 278130   | 54368      | 47393 |
| O       | 272095   | 56774      | 44682 |
| F       | 32945    | 7026       | 7296  |
| P       | 5422     | 1522       | 3103  |
| S       | 82938    | 17168      | 12226 |
| Cl      | 34440    | 7682       | 5838  |
| Br      | 15813    | 2486       | 1482  |
| I       | 2986     | 412        | 239   |

#### Total charges

| Charge | Training | Validation | Test  |
|--------|----------|------------|-------|
| -6     | 4        | 0          | 2     |
| -5     | 7        | 0          | 14    |
| -4     | 209      | 27         | 154   |
| -3     | 455      | 66         | 1040  |
| -2     | 3747     | 902        | 1333  |
| -1     | 25826    | 7553       | 3441  |
| 0      | 216930   | 41211      | 39450 |
| 1      | 56354    | 10692      | 7118  |
| 2      | 6999     | 1080       | 471   |
| 3      | 508      | 55         | 21    |
| 4      | 70       | 6          | 1     |
| 5      | 1        | 1          | 0     |
| 6      | 1        | 0          | 0     |
| 7      | 0        | 0          | 0     |
| 8      | 2        | 0          | 0     |

#### Number of atoms

| # Atoms | Training | Validation | Test  |
|---------|----------|------------|-------|
| 000-009 | 363      | 7          | 319   |
| 010-019 | 15322    | 421        | 4342  |
| 020-029 | 63828    | 6925       | 15237 |
| 030-039 | 103631   | 25430      | 9189  |
| 040-049 | 86267    | 22697      | 11165 |
| 050-059 | 24808    | 5747       | 4343  |
| 060-069 | 8631     | 347        | 700   |
| 070-079 | 6100     | 19         | 103   |
| 080-089 | 1948     | 0          | 60    |
| 090-099 | 215      | 0          | 647   |
| 100-109 | 0        | 0          | 2104  |
| 110-119 | 0        | 0          | 1833  |
| 120-129 | 0        | 0          | 873   |
| 130-139 | 0        | 0          | 977   |
| 140-149 | 0        | 0          | 702   |
| 150-159 | 0        | 0          | 430   |
| 160-169 | 0        | 0          | 21    |

#### Number of heavy atoms

| # Atoms | Training | Validation | Test  |
|---------|----------|------------|-------|
| 000-009 | 6147     | 44         | 3056  |
| 010-019 | 131447   | 18303      | 21270 |
| 020-029 | 156412   | 43246      | 16915 |
| 030-039 | 14183    | 0          | 4114  |
| 040-049 | 2859     | 0          | 743   |
| 050-059 | 65       | 0          | 3417  |
| 060-069 | 0        | 0          | 3330  |
| 070-079 | 0        | 0          | 198   |
| 080-089 | 0        | 0          | 2     |



## Acknowledgements

We gratefully acknowledge the following people and organisations who helped us with the data used for training, validation, and testing:

- Enamine
- [Patrick Bleiziffer, Kay Schaller, and Sereina Riniker][riniker]
- The Open NCI Database
- The Ligand Expo and Protein Data Bank (PDB)
- MolSSI
- Peter Eastman, Pavan Kumar Behara, David L. Dotson, Raimondas Galvelis, John E. Herr, Josh T. Horton, Yuezhi Mao, John D. Chodera, Benjamin P. Pritchard, Yuanqing Wang, Gianni De Fabritiis, and Thomas E. Markland. "SPICE, A Dataset of Drug-like Molecules and Peptides for Training Machine Learning Potentials." Scientific Data 10, 11 (2023). https://doi.org/10.1038/s41597-022-01882-6
- RDKit
- the ChEMBL database
