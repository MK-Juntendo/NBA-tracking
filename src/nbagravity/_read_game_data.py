import json


def _read_file(file_path):
    with open(file_path) as f:
        raw_data = json.load(f)
    assert list(raw_data.keys()) == ['gameid', 'gamedate', 'events']

    return raw_data


def _format_game_info(raw_data):
    game_info = {}
    game_info["gameid"], game_info["gamedate"] = raw_data["gameid"], raw_data["gamedate"]
    events = raw_data["events"]

    eventIds = []
    visitor = events[0]["visitor"]
    home = events[0]["home"]
    for event in events:
        eventIds.append(int(event["eventId"]))
        assert event["visitor"] == visitor
        assert event["home"] == home
        
    assert len(eventIds) == len(set(eventIds))  # check uniqueness of eventIds
    game_info["eventId_num"] = len(eventIds)
    game_info["eventId_begin"] = min(eventIds)
    game_info["eventId_end"] = max(eventIds)

    game_info["visitor_team_name"] = visitor["name"]
    game_info["visitor_team_id"] = visitor["teamid"]
    game_info["visitor_team_abbr"] = visitor["abbreviation"]
    game_info["visitor_players"] = visitor["players"]
    game_info["home_team_name"] = home["name"]
    game_info["home_team_id"] = home["teamid"]
    game_info["home_team_abbr"] = home["abbreviation"]
    game_info["home_players"] = home["players"]

    return game_info


def _format_tracking_data(events):
    frames = {}
    for movieId, event in enumerate(events):
        eventId = event["eventId"]

        for moment in event["moments"]:
            quater = moment[0]
            unixtime = moment[1]
            quatertime = moment[2]
            shotclock = moment[3]
            assert moment[4] == None
            position = moment[5]

            assert type(unixtime) == int
            assert quater in [1, 2, 3, 4]
            assert 0 <= quatertime <= 720
            if shotclock:
                assert 0 <= shotclock <= 24

            if position[0][0:2] != [-1, -1]:  # first-aid to avoid duplication
                print(f"Warning: skipped <unixtime: {unixtime}, movieId: {movieId}, eventId: {eventId}> it does not have ball position data")
                continue

            if unixtime not in frames.keys():
                _frame = {}
                _frame["movieId"] = [movieId]
                _frame["eventId"] = [eventId]
                _frame["quater"] = quater
                _frame["quatertime"] = quatertime
                _frame["shotclock"] = shotclock
                _frame["position"] = position

                frames[unixtime] = _frame
            else:
                assert quater == frames[unixtime]["quater"]
                assert quatertime == frames[unixtime]["quatertime"]
                assert shotclock == frames[unixtime]["shotclock"]
                assert position == frames[unixtime]["position"]

                assert movieId not in frames[unixtime]["movieId"]
                assert eventId not in frames[unixtime]["eventId"]
                frames[unixtime]["movieId"].append(movieId)
                frames[unixtime]["eventId"].append(eventId)

    result = []
    for unixtime in frames.keys():
        _frame = dict(**{"unixtime": unixtime / 1000}, **frames[unixtime])
        result.append(_frame)

    return result


def read_game_info(file_path):
    raw_data = _read_file(file_path)
    game_info = _format_game_info(raw_data)

    return game_info 


def read_tracking_data(file_path):
    raw_data = _read_file(file_path)
    events = raw_data["events"]

    tracking_data = _format_tracking_data(events)

    return tracking_data
