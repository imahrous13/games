import sys
import math
import random
import numpy as np
import pygame

# -------- Colors --------
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# -------- Board config --------
ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4


# ==============================
# Core game logic
# ==============================
def create_board():
    # Use ints, not floats
    return np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    # Topmost cell in the column must be empty to allow a drop
    return board[ROW_COUNT - 1][col] == EMPTY


def get_next_open_row(board, col):
    # Find the lowest available row in a column
    for r in range(ROW_COUNT):
        if board[r][col] == EMPTY:
            return r
    return None  # column full


def print_board(board):
    # Flip vertically so the "bottom" prints last
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Horizontal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True

    # Vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True

    # Positive slope diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True

    # Negative slope diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                return True

    return False


def get_winning_sequence(board, piece):
    """Return a list of four (r,c) cells if 'piece' has won, else None."""
    # Horizontal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            seq = [(r, c + i) for i in range(4)]
            if all(board[r][c + i] == piece for i in range(4)):
                return seq

    # Vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            seq = [(r + i, c) for i in range(4)]
            if all(board[r + i][c] == piece for i in range(4)):
                return seq

    # Positive diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            seq = [(r + i, c + i) for i in range(4)]
            if all(board[r + i][c + i] == piece for i in range(4)):
                return seq

    # Negative diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            seq = [(r - i, c + i) for i in range(4)]
            if all(board[r - i][c + i] == piece for i in range(4)):
                return seq

    return None


# ==============================
# Heuristics & Minimax
# ==============================
def evaluate_window(window, piece):
    """Score a 4-cell window."""
    if not isinstance(window, list):
        window = list(window)

    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    # Block opponent's three-in-a-row with an open end
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    """Heuristic board evaluation function."""
    score = 0

    # Center column preference
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Horizontal score
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c : c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Vertical score
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r : r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Positive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [int(board[r + i][c + i]) for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Negative sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [int(board[r + 3 - i][c + i]) for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def get_valid_locations(board):
    return [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]


def is_terminal_node(board):
    return (
        winning_move(board, PLAYER_PIECE)
        or winning_move(board, AI_PIECE)
        or len(get_valid_locations(board)) == 0
    )


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    terminal = is_terminal_node(board)

    if depth == 0 or terminal:
        if terminal:
            if winning_move(board, AI_PIECE):
                return (None, float("inf"))
            elif winning_move(board, PLAYER_PIECE):
                return (None, float("-inf"))
            else:
                return (None, 0)  # Draw
        else:
            return (None, score_position(board, AI_PIECE))

    if maximizingPlayer:
        value = float("-inf")
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            if row is None:
                continue
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value

    else:
        value = float("inf")
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            if row is None:
                continue
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value


# ==============================
# Pygame drawing
# ==============================
def cell_center_pixels(c, r, SQUARESIZE, height):
    """Get (x,y) pixel center for board cell (r,c)."""
    x = int(c * SQUARESIZE + SQUARESIZE / 2)
    y = height - int(r * SQUARESIZE + SQUARESIZE / 2)  # flip vertically for display
    return x, y


def draw_board(board, screen, SQUARESIZE, RADIUS, height, winning_seq=None):
    # Board background + empty circles
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(
                screen,
                BLUE,
                (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE),
            )
            pygame.draw.circle(
                screen,
                BLACK,
                (
                    int(c * SQUARESIZE + SQUARESIZE / 2),
                    int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2),
                ),
                RADIUS,
            )

    # Pieces
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            value = board[r][c]
            if value == PLAYER_PIECE:
                color = RED
            elif value == AI_PIECE:
                color = YELLOW
            else:
                continue

            pygame.draw.circle(
                screen,
                color,
                (
                    int(c * SQUARESIZE + SQUARESIZE / 2),
                    height - int(r * SQUARESIZE + SQUARESIZE / 2),
                ),
                RADIUS,
            )

    # If there is a winning sequence, highlight it
    if winning_seq:
        points = []
        for r, c in winning_seq:
            cx, cy = cell_center_pixels(c, r, SQUARESIZE, height)
            points.append((cx, cy))
            # outline around winning discs
            pygame.draw.circle(screen, WHITE, (cx, cy), RADIUS, width=6)

        # line through the sequence
        if len(points) >= 2:
            pygame.draw.line(screen, WHITE, points[0], points[-1], width=6)

    pygame.display.update()


# ==============================
# Main
# ==============================
def main():
    board = create_board()
    print_board(board)
    game_over = False

    pygame.init()

    SQUARESIZE = 100
    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE
    size = (width, height)
    RADIUS = int(SQUARESIZE / 2 - 5)

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Connect 4 — Player vs AI")
    draw_board(board, screen, SQUARESIZE, RADIUS, height)

    myfont = pygame.font.SysFont("monospace", 60)

    # Randomly choose who starts
    turn = random.randint(PLAYER, AI)

    winning_seq = None  # will store winning coords when game ends

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Hover indicator for the player
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

            # Player move
            if event.type == pygame.MOUSEBUTTONDOWN:
                if turn == PLAYER and not game_over:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    col = posx // SQUARESIZE  # integer division to get column

                    if 0 <= col < COLUMN_COUNT and is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        if row is not None:
                            drop_piece(board, row, col, PLAYER_PIECE)

                            if winning_move(board, PLAYER_PIECE):
                                winning_seq = get_winning_sequence(board, PLAYER_PIECE)
                                label = myfont.render("Player wins!!", True, RED)
                                screen.blit(label, (40, 10))
                                draw_board(
                                    board,
                                    screen,
                                    SQUARESIZE,
                                    RADIUS,
                                    height,
                                    winning_seq=winning_seq,
                                )
                                # Blink highlight so opponent clearly sees it
                                for _ in range(4):
                                    pygame.time.wait(250)
                                    draw_board(
                                        board,
                                        screen,
                                        SQUARESIZE,
                                        RADIUS,
                                        height,
                                        winning_seq=None,
                                    )
                                    pygame.time.wait(250)
                                    draw_board(
                                        board,
                                        screen,
                                        SQUARESIZE,
                                        RADIUS,
                                        height,
                                        winning_seq=winning_seq,
                                    )
                                game_over = True

                            print_board(board)
                            if not game_over:
                                draw_board(board, screen, SQUARESIZE, RADIUS, height)

                            turn = AI  # switch turn

        # AI move
        if turn == AI and not game_over:
            col, _ = minimax(
                board,
                depth=5,
                alpha=float("-inf"),
                beta=float("inf"),
                maximizingPlayer=True,
            )

            if col is not None and is_valid_location(board, col):
                row = get_next_open_row(board, col)
                if row is not None:
                    drop_piece(board, row, col, AI_PIECE)

                    if winning_move(board, AI_PIECE):
                        winning_seq = get_winning_sequence(board, AI_PIECE)
                        label = myfont.render("AI wins!!", True, YELLOW)
                        screen.blit(label, (40, 10))
                        draw_board(
                            board,
                            screen,
                            SQUARESIZE,
                            RADIUS,
                            height,
                            winning_seq=winning_seq,
                        )
                        for _ in range(4):
                            pygame.time.wait(250)
                            draw_board(
                                board,
                                screen,
                                SQUARESIZE,
                                RADIUS,
                                height,
                                winning_seq=None,
                            )
                            pygame.time.wait(250)
                            draw_board(
                                board,
                                screen,
                                SQUARESIZE,
                                RADIUS,
                                height,
                                winning_seq=winning_seq,
                            )
                        game_over = True

                    print_board(board)
                    if not game_over:
                        draw_board(board, screen, SQUARESIZE, RADIUS, height)

                    turn = PLAYER  # switch turn

        if game_over:
            pygame.display.update()
            pygame.time.wait(1500)


if __name__ == "__main__":
    main()
