import pytest
from app.bll.types import AgentType
from app.bll.game_utils import change_player


def test_change_player():
    # Test switching from RED to BLUE
    assert change_player(AgentType.RED) == AgentType.BLUE

    # Test switching from BLUE to RED
    assert change_player(AgentType.BLUE) == AgentType.RED

    # Ensure function only works with valid TeamColor types
    invalid_player = "INVALID_PLAYER"
    with pytest.raises(ValueError):
        change_player(
            invalid_player
        )  # Should raise an error since the type isn't valid
