import math
from dataclasses import dataclass

# --- YOUR CODE ---

_EPS = 1e-3

def alpha_beta_search(game, state):
    """Return the best action for the player to move in `state`."""
    nodes = [0]
    player = game.to_move(state)
    actions = game.actions(state)

    if not actions:
        alpha_beta_search.last_node_count = 1
        alpha_beta_search.last_value = game.utility(state)
        return None

    best_action = None

    if player == 'MAX':
        best_value = -math.inf
        alpha, beta = -math.inf, math.inf

        for action in actions:
            child = game.result(state, action)
            value = _value(game, child, alpha, beta, nodes, depth=1)

            if value > best_value:
                best_value = value
                best_action = action

            alpha = max(alpha, best_value)

    else:  # MIN
        best_value = math.inf
        alpha, beta = -math.inf, math.inf

        for action in actions:
            child = game.result(state, action)
            value = _value(game, child, alpha, beta, nodes, depth=1)

            if value < best_value:
                best_value = value
                best_action = action

            beta = min(beta, best_value)

    # include the root call in the count
    alpha_beta_search.last_node_count = nodes[0] + 1
    alpha_beta_search.last_value = best_value
    return best_action


def _value(game, state, alpha, beta, nodes, depth=0):
    """Recursive helper. Increment nodes[0] once per call.
    Return the minimax value of `state`."""
    nodes[0] += 1

    if game.is_terminal(state):
        u = game.utility(state)

        # Tie-break on depth:
        # prefer faster wins and slower losses.
        if u > 0:
            return u - _EPS * depth
        if u < 0:
            return u + _EPS * depth
        return 0

    if game.to_move(state) == 'MAX':
        v = -math.inf
        for action in game.actions(state):
            child = game.result(state, action)
            v = max(v, _value(game, child, alpha, beta, nodes, depth + 1))
            alpha = max(alpha, v)
            if alpha >= beta:
                break
        return v

    else:  # MIN
        v = math.inf
        for action in game.actions(state):
            child = game.result(state, action)
            v = min(v, _value(game, child, alpha, beta, nodes, depth + 1))
            beta = min(beta, v)
            if alpha >= beta:
                break
        return v

# --- DO NOT MODIFY BELOW ---

class Game:
    def initial_state(self): ...
    def to_move(self, state): ...          # returns 'MAX' or 'MIN'
    def actions(self, state): ...          # list of legal moves
    def result(self, state, action): ...   # returns new state
    def is_terminal(self, state): ...
    def utility(self, state): ...          # from MAX's perspective

@dataclass(frozen=True)
class TTTState:
    board: tuple        # 9-tuple of 'X', 'O', or '.'
    player: str         # 'X' (MAX) or 'O' (MIN)

class TicTacToe(Game):
    LINES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

    def initial_state(self):
        return TTTState(('.',)*9, 'X')

    def to_move(self, s):
        return 'MAX' if s.player == 'X' else 'MIN'

    def actions(self, s):
        return [i for i, c in enumerate(s.board) if c == '.']

    def result(self, s, a):
        b = list(s.board); b[a] = s.player
        return TTTState(tuple(b), 'O' if s.player == 'X' else 'X')

    def _winner(self, s):
        for i,j,k in self.LINES:
            if s.board[i] != '.' and s.board[i]==s.board[j]==s.board[k]:
                return s.board[i]
        return None

    def is_terminal(self, s):
        return self._winner(s) is not None or '.' not in s.board

    def utility(self, s):
        w = self._winner(s)
        return 1 if w == 'X' else -1 if w == 'O' else 0