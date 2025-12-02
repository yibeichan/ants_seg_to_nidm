from pathlib import Path

from ants_seg_to_nidm.antsutils import read_ants_stats

EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples"


def test_read_ants_stats_returns_expected_measurements():
    measures = read_ants_stats(
        EXAMPLES_DIR / "antslabelstats.csv",
        EXAMPLES_DIR / "antsbrainvols.csv",
        EXAMPLES_DIR / "antsBrainSegmentation.nii.gz",
        force_error=False,
    )
    assert len(measures) == 103
    measure_map = dict(measures)
    # spot-check a volumetric measurement (in mm^3) that relies on voxel size conversion
    assert measure_map["000002"] == "1666780"
    # ensure fractional values are preserved for non-volume metrics
    assert measure_map["000001"].startswith("0.83")
