import numpy as np


def separate_positions(positions, teamid_visitor, teamid_home):
    assert positions[0][0:2] == [-1, -1]
    position_ball = np.array(positions[0][2:4])

    positions_visitor = []
    positions_home = []

    for position in positions[1:]:
        if position[0] == teamid_visitor:
            positions_visitor.append(np.array(position[2:4]))
        elif position[0] == teamid_home:
            positions_home.append(np.array(position[2:4]))
        else:
            raise Exception

    if len(positions_visitor) == 0 or len(positions_home) == 0:
        print(f"Warning: positions data is nothing")

    result = {"position_ball": position_ball, "positions_visitor": positions_visitor, "positions_home": positions_home}

    return result
