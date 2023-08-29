import pytest
import numpy as np

pytest.importorskip("openff.nagl")


@pytest.mark.parametrize(
    "model_file, expected_charges",
    [
        (
            "openff-gnn-am1bcc-0.0.1-alpha.1.pt",
            [-0.119291  ,  0.12953702, -0.60555816,  0.04394022, 
             0.04394018, 0.04394022,  0.03412103,  0.034121  ,
               0.39524958]
        ),
        (
            "openff-gnn-am1bcc-0.1.0-rc.1.pt",
            [-0.101634,  0.133269, -0.605404, 
             0.043411,  0.043411,  0.043411,
             0.019863,  0.019863,  0.40381 ]
        )
    ]
)
def test_models_ethanol(model_file, expected_charges):
    from openff.nagl.nn._models import GNNModel
    from openff.toolkit import Molecule
    from openff.nagl_models import validate_nagl_model_path

    model_path = validate_nagl_model_path(model_file)
    model = GNNModel.load(model_path, eval_mode=True)
    ethanol = Molecule.from_smiles("CCO")
    charges = model.compute_property(
        ethanol,
        readout_name="am1bcc_charges",
        as_numpy=True
    )
    np.testing.assert_allclose(charges, expected_charges, atol=1e-5)
