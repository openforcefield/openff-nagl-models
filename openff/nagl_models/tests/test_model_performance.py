import numpy as np
import pytest

pytest.importorskip("openff.nagl")


@pytest.mark.parametrize(
    "model_file, expected_charges",
    [
        (
            "openff-gnn-am1bcc-0.0.1-alpha.1.pt",
            [
                -0.119291,
                0.12953702,
                -0.60555816,
                0.04394022,
                0.04394018,
                0.04394022,
                0.03412103,
                0.034121,
                0.39524958,
            ],
        ),
        (
            "openff-gnn-am1bcc-0.1.0-rc.1.pt",
            [
                -0.101634,
                0.133269,
                -0.605404,
                0.043411,
                0.043411,
                0.043411,
                0.019863,
                0.019863,
                0.40381,
            ],
        ),
        (
            "openff-gnn-am1bcc-0.1.0-rc.2.pt",
            [
                -0.111519,
                0.133221,
                -0.60017,
                0.044064,
                0.044064,
                0.044064,
                0.022841,
                0.022841,
                0.400592,
            ],
        ),
        (
            "openff-gnn-am1bcc-0.1.0-rc.3.pt",
            [
                -0.09629,
                0.13245,
                -0.60293,
                0.04465,
                0.04465,
                0.04465,
                0.01728,
                0.01728,
                0.39826,
            ],
        ),
        (
            "openff-gnn-am1bcc-1.0.0.pt",
            [
                -0.09629,
                0.13245,
                -0.60293,
                0.04465,
                0.04465,
                0.04465,
                0.01728,
                0.01728,
                0.39826,
            ],
        ),
    ],
)
def test_models_ethanol(model_file, expected_charges):
    from openff.nagl.nn._models import GNNModel
    from openff.nagl_models import validate_nagl_model_path
    from openff.toolkit import Molecule

    model_path = validate_nagl_model_path(model_file)
    model = GNNModel.load(model_path, eval_mode=True)
    ethanol = Molecule.from_smiles("CCO")
    charges = model.compute_property(ethanol, readout_name="am1bcc_charges", as_numpy=True)
    np.testing.assert_allclose(charges, expected_charges, atol=1e-5)
