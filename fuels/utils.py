import re
from lat_lon_parser import parse


dms_re = r"[+-]?[0-9]{1,3}\s?°\s?[0-9]{1,3}\s?'\s?[0-9]{1,3}[\.]?[0-9]{0,3}\s?\"\s?[E,W,N,S]?"
ddm_re = r"[+-]?[0-9]{1,3}\s?°\s?[0-9]{1,3}\.[0-9]{3,10}\s?[E,W,N,S]?"
dd_re = r"[+-]?[0-9]{1,3}\.[0-9]{2,10}\s?[E,W,N,S]?"

patterns = dict(dms=dms_re, ddm=ddm_re, dd=dd_re)


def parse_coords(coords: str):
    for format_, pattern in patterns.items():
        matched_coords = re.findall(pattern, coords)
        if len(matched_coords) == 2:
            # print("Detected format", format_, matched_coords)
            break
    assert len(matched_coords) == 2, "Can't detect location format"
    matched_coords = [parse(c) for c in matched_coords]
    return matched_coords


def parse_coords_test():
    eps = 1e-4
    true = [41.40338, 2.17403]
    examples = [" 41.40338,2.17403",
                """41°24'12.2"N 2°10'26.5"E""",
                """41°24.202,     2°10.4418""",
                "41° 24.202', 2° 10.4418'",
                """41° 24' 12.2", 2° 10' 26.5"E """]
    for e in examples:
        parsed = parse_coords(e)
        assert all(abs(p - t) < eps for p, t in zip(parsed, true))

if __name__ == '__main__':
    parse_coords_test()
