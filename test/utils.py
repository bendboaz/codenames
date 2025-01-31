from app.bll.board import AgentPlacements, Board
from app.bll.types import Card, AgentType


def get_test_board():
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
    return board
