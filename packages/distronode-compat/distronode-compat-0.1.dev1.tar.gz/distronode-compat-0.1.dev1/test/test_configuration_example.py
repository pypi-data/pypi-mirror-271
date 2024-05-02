"""Sample usage of DistronodeConfig."""
from distronode_compat.config import DistronodeConfig


def test_example_config() -> None:
    """Test basic functionality of DistronodeConfig."""
    cfg = DistronodeConfig()
    assert isinstance(cfg.ACTION_WARNINGS, bool)
    # you can also use lowercase:
    assert isinstance(cfg.action_warnings, bool)
    # you can also use it as dictionary
    assert cfg["action_warnings"] == cfg.action_warnings
