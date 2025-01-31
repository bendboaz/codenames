import pytest
from app.bll.types import GameEndStatus, Card
from app.bll.board import Board, AgentPlacements
from app.bll.defaults import DEFAULT_BOARD_SIZE
from app.bll.types import AgentType, Coordinate
from test.utils import get_test_board


def test_agent_placements_shadow_board():
    positions = {
        AgentType.RED: [Coordinate.from_tuple(0, 0), Coordinate.from_tuple(1, 1)],
        AgentType.BLUE: [Coordinate.from_tuple(2, 2)],
    }

    agent_placements = AgentPlacements(
        positions=positions, starting_color=AgentType.RED
    )

    # Validate shadow board is correctly built
    assert agent_placements.shadow_board[0][0] == AgentType.RED
    assert agent_placements.shadow_board[1][1] == AgentType.RED
    assert agent_placements.shadow_board[2][2] == AgentType.BLUE

    # Check that non-specified coordinates default to INNOCENT
    assert agent_placements.shadow_board[3][3] == AgentType.INNOCENT


def test_agent_placements_build_shadow_board_static():
    positions = {
        AgentType.RED: [Coordinate.from_tuple(0, 0), Coordinate.from_tuple(1, 1)],
        AgentType.BLUE: [Coordinate.from_tuple(2, 2)],
    }

    agent_placements = AgentPlacements(
        positions=positions, starting_color=AgentType.RED
    )

    shadow_board = agent_placements.build_shadow_board_static()

    # Validate positions are correctly placed in the shadow board
    assert shadow_board[0][0] == AgentType.RED
    assert shadow_board[1][1] == AgentType.RED
    assert shadow_board[2][2] == AgentType.BLUE

    # Check that unoccupied spaces remain INNOCENT
    assert shadow_board[3][3] == AgentType.INNOCENT


def test_agent_placements_random():
    random_seed = 42  # Use a fixed seed for deterministic behavior
    agent_placements = AgentPlacements.random(random_seed=random_seed)

    # Validate the starting color is one of the valid options
    assert agent_placements.starting_color in [AgentType.RED, AgentType.BLUE]

    # Validate the total number of agents
    total_agents = sum(len(coords) for coords in agent_placements.positions.values())
    assert total_agents == DEFAULT_BOARD_SIZE**2


def test_agent_placements_getitem():
    positions = {
        AgentType.RED: [Coordinate.from_tuple(0, 0)],
        AgentType.BLUE: [Coordinate.from_tuple(1, 1)],
    }
    agent_placements = AgentPlacements(
        positions=positions, starting_color=AgentType.RED
    )

    # Validate that __getitem__ fetches the correct agent
    assert agent_placements[Coordinate.from_tuple(0, 0)] == AgentType.RED
    assert agent_placements[Coordinate.from_tuple(1, 1)] == AgentType.BLUE

    # Check fallback to INNOCENT
    assert agent_placements[Coordinate.from_tuple(2, 2)] == AgentType.INNOCENT


def test_board_initialization_valid():
    words = [
        ["word1", "word2", "word3", "word4", "word5"],
        ["word6", "word7", "word8", "word9", "word10"],
        ["word11", "word12", "word13", "word14", "word15"],
        ["word16", "word17", "word18", "word19", "word20"],
        ["word21", "word22", "word23", "word24", "word25"],
    ]
    agent_placements = AgentPlacements.random(random_seed=42)

    board = Board.from_words_and_placements(words=words, placements=agent_placements)

    # Validate board dimensions and structure
    assert [[word.word for word in row] for row in board.words] == words
    assert len(board.words) == 5
    assert len(board.words[0]) == 5


def test_board_initialization_invalid():
    words = [
        ["word1", "word2", "word3"],
        ["word4", "word5"],  # Non-uniform row length
    ]
    agent_placements = AgentPlacements.random(random_seed=42)

    with pytest.raises(ValueError, match="The words array must be a square array."):
        Board.from_words_and_placements(words=words, placements=agent_placements)


def test_board_discovered_agents():
    words = [
        ["word1", "word2", "word3", "word4", "word5"],
        ["word6", "word7", "word8", "word9", "word10"],
        ["word11", "word12", "word13", "word14", "word15"],
        ["word16", "word17", "word18", "word19", "word20"],
        ["word21", "word22", "word23", "word24", "word25"],
    ]
    words = [
        [Card(word=word, card_type=AgentType.UNKNOWN) for word in row] for row in words
    ]
    agent_placements = AgentPlacements.random(random_seed=42)
    discovered_agents = [Coordinate.from_tuple(1, 1), Coordinate.from_tuple(2, 2)]

    board = Board(
        words=words,
        agent_placements=agent_placements,
        discovered_agents=discovered_agents,
    )

    # Validate discovered agents are set correctly
    assert board.discovered_agents == discovered_agents
    assert len(board.discovered_agents) == 2


def test_board_random_with_words():
    words = [
        "word1",
        "word2",
        "word3",
        "word4",
        "word5",
        "word6",
        "word7",
        "word8",
        "word9",
        "word10",
        "word11",
        "word12",
        "word13",
        "word14",
        "word15",
        "word16",
        "word17",
        "word18",
        "word19",
        "word20",
        "word21",
        "word22",
        "word23",
        "word24",
        "word25",
    ]

    # Create a board using the random_with_words method with a fixed seed
    board = Board.random_with_words(words=words, random_seed=42)

    # Verify that words are reshaped into a 5x5 grid (DEFAULT_BOARD_SIZE assumed as 5)
    assert len(board.words) == 5
    assert all(len(row) == 5 for row in board.words)

    # Verify that all input words are present, but order is shuffled
    flattened_result = [card.word for row in board.words for card in row]
    assert sorted(flattened_result) == sorted(words)

    # Verify all card states are set as UNKNOWN
    for row in board.words:
        for card in row:
            assert card.card_type == AgentType.UNKNOWN

    # Verify it created the agent placements
    assert isinstance(board.agent_placements, AgentPlacements)


def test_board_reveal_card():
    from app.bll.types import Card, AgentType

    words = [
        [
            Card(word="word1", card_type=AgentType.UNKNOWN),
            Card(word="word2", card_type=AgentType.UNKNOWN),
        ],
        [
            Card(word="word3", card_type=AgentType.UNKNOWN),
            Card(word="word4", card_type=AgentType.UNKNOWN),
        ],
    ]
    agent_placements = AgentPlacements.random(random_seed=42)
    board = Board(words=words, agent_placements=agent_placements)

    coord = Coordinate.from_tuple(0, 0)
    agent_type = board.reveal_card(coord)

    # Validate discovered agents list
    assert coord in board.discovered_agents

    # Validate agent type from placements
    assert agent_type == board.agent_placements[coord]

    # Validate the card's type is updated
    updated_card = board.words[coord.x][coord.y]
    assert updated_card.card_type == agent_type


def test_check_game_end_ongoing():
    words = [
        ["word1", "word2", "word3", "word4", "word5"],
        ["word6", "word7", "word8", "word9", "word10"],
        ["word11", "word12", "word13", "word14", "word15"],
        ["word16", "word17", "word18", "word19", "word20"],
        ["word21", "word22", "word23", "word24", "word25"],
    ]
    agent_placements = AgentPlacements.random(random_seed=42)
    board = Board.from_words_and_placements(words=words, placements=agent_placements)

    game_status = board.check_game_end()

    # Validate that the game is still ongoing
    assert game_status == GameEndStatus.ONGOING


def test_check_game_end_victory():
    from app.bll.types import AgentType

    words = [
        ["word1", "word2", "word3", "word4", "word5"],
        ["word6", "word7", "word8", "word9", "word10"],
        ["word11", "word12", "word13", "word14", "word15"],
        ["word16", "word17", "word18", "word19", "word20"],
        ["word21", "word22", "word23", "word24", "word25"],
    ]

    positions = {
        AgentType.RED: [Coordinate.from_tuple(0, 0)],
        AgentType.BLUE: [Coordinate.from_tuple(1, 1)],
        AgentType.BLACK: [Coordinate.from_tuple(4, 4)],
        AgentType.INNOCENT: [],
    }
    agent_placements = AgentPlacements(
        positions=positions, starting_color=AgentType.RED
    )
    board = Board.from_words_and_placements(words=words, placements=agent_placements)

    # Reveal all RED agents
    board.reveal_card(Coordinate.from_tuple(0, 0))

    game_status = board.check_game_end()

    # Validate that BLUE wins when all RED agents are revealed
    assert game_status == GameEndStatus.RED_VICTORY


def test_check_game_end_black_card():
    from app.bll.types import AgentType

    words = [
        ["word1", "word2", "word3", "word4", "word5"],
        ["word6", "word7", "word8", "word9", "word10"],
        ["word11", "word12", "word13", "word14", "word15"],
        ["word16", "word17", "word18", "word19", "word20"],
        ["word21", "word22", "word23", "word24", "word25"],
    ]

    positions = {
        AgentType.RED: [Coordinate.from_tuple(0, 0)],
        AgentType.BLUE: [Coordinate.from_tuple(1, 1)],
        AgentType.BLACK: [Coordinate.from_tuple(4, 4)],
        AgentType.INNOCENT: [],
    }
    agent_placements = AgentPlacements(
        positions=positions, starting_color=AgentType.RED
    )
    board = Board.from_words_and_placements(words=words, placements=agent_placements)

    # Reveal the BLACK agent
    board.reveal_card(Coordinate.from_tuple(4, 4))

    game_status = board.check_game_end()

    # Validate that the game ends when the BLACK card is revealed
    assert game_status == GameEndStatus.BLACK_REVEALED


def test_board_reveal_card_out_of_bounds():
    words = [
        [
            Card(word="word1", card_type=AgentType.UNKNOWN),
            Card(word="word2", card_type=AgentType.UNKNOWN),
        ],
        [
            Card(word="word3", card_type=AgentType.UNKNOWN),
            Card(word="word4", card_type=AgentType.UNKNOWN),
        ],
    ]
    agent_placements = AgentPlacements.random(random_seed=42)
    board = Board(words=words, agent_placements=agent_placements)

    # Attempt to reveal a card outside the board's bounds
    out_of_bounds_coord = Coordinate.from_tuple(3, 3)  # Out of bounds
    with pytest.raises(ValueError, match="The guessed coordinate is out of bounds."):
        board.reveal_card(out_of_bounds_coord)


def test_board_reveal_card_already_revealed():
    board = get_test_board()

    coord = Coordinate.from_tuple(0, 0)

    # Reveal the card for the first time
    board.reveal_card(coord)

    # Attempt to reveal the same card again, expecting an error
    with pytest.raises(ValueError, match="This coordinate has already been revealed."):
        board.reveal_card(coord)
