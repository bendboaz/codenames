from app.bll.types import Card


def format_card_word(card: Card) -> str:
    """
    Formats the card to display only its word.

    :param card: A Card object to format.
    :return: A string with the card's word.
    """
    return f"{card.word}"


def format_card_type(card: Card) -> str:
    """
    Formats the card to display only its card_type.

    :param card: A Card object to format.
    :return: A string with the card's card_type.
    """
    return f"{card.card_type.value}"


def show_words(words: list[list[Card]]):
    """
    Displays the 2D array of Cards with the word in one row and the card type in the next row.
    Each row is aligned properly.

    :param words: A 2D list of Card objects representing the game board.
    """
    # Calculate maximum width for each column based on the longest word and card type separately
    col_widths = [
        max(
            max(len(format_card_word(row[col])) for row in words),
            max(len(format_card_type(row[col])) for row in words),
        )
        for col in range(len(words[0]))
    ]
    max_col_width = max(col_widths)

    for row in words:
        print(
            " | ".join(
                format_card_word(card).center(max_col_width)
                for col, card in enumerate(row)
            )
        )
        print(
            " | ".join(
                format_card_type(card).center(max_col_width)
                for col, card in enumerate(row)
            )
        )

        # Print a line separator for clarity
        print("-" * (max_col_width * len(words[0]) + (3 * (len(words[0]) - 1))))
