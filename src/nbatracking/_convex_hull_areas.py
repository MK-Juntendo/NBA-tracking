from scipy.spatial import ConvexHull

from nbatracking import separate_positions


def _caluculate_convex_hull_area_moment(positions, teamid_visitor, teamid_home):
    positions_separated = separate_positions(positions, teamid_visitor, teamid_home)
    positions_visitor = positions_separated["positions_visitor"]
    positions_home = positions_separated["positions_home"]

    if len(positions_visitor) == 0:
        area_visitor = None
    else:
        area_visitor = ConvexHull(positions_visitor).area
    if len(positions_home) == 0:
        area_home = None
    else:
        area_home = ConvexHull(positions_home).area

    result = {"convex_hull_area_visitor": area_visitor, "convex_hull_area_home": area_home}
    return result


def caluculate_convex_hull_areas(positions_set, teamid_visitor, teamid_home):
    areas_visitor = []
    areas_home = []
    for positions in positions_set:
        areas = _caluculate_convex_hull_area_moment(positions, teamid_visitor, teamid_home)
        areas_visitor.append(areas["convex_hull_area_visitor"])
        areas_home.append(areas["convex_hull_area_home"])

    result = {"convex_hull_area_visitor": areas_visitor, "convex_hull_area_home": areas_home}

    return result
