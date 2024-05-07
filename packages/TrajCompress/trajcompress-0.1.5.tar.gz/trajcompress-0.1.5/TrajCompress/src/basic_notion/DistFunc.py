from .Point import Point
import math


def perpendicular_euclidean_dist(start_point: Point, mid_point: Point, end_point: Point) -> float:
    """
    Step 1: Find the nearest point, p', of mid_point, on the line start_point - end_point
    Step 2: Calculate the Euclidean distance between mid_point and p'
    Note: The distance calculation is based on x-y-z Cartesian coordinate system --
          Please check Point.latlon2cartesian() before calling this function
                                  o (mid_point)
                                  |
        (start_point) o ----------o--- o (end_point)
                                  p'
    """
    start_x, start_y, start_z = start_point.get_cx(), start_point.get_cy(), start_point.get_cz()
    end_x, end_y, end_z = end_point.get_cx(), end_point.get_cy(), end_point.get_cz()
    mid_x, mid_y, mid_z = mid_point.get_cx(), mid_point.get_cy(), mid_point.get_cz()

    if any(val is None for val in [start_x, start_y, start_z, end_x, end_y, end_z, mid_x, mid_y, mid_z]):
        print("Distance calculation needs coordinate coversion from lat/lon to Cartesian one")
        exit()

    vec_start_mid = (mid_x - start_x, mid_y - start_y, mid_z - start_z)
    vec_start_end = (end_x - start_x, end_y - start_y, end_z - start_z)

    # dot_product_start2mid_start2end = |start-mid| |start-end| cos(\theta)
    # (\theta is the angle between start-mid and start-end)
    # norm_vec_start2end = |start-end| |start-end|
    dot_product_start2mid_start2end = sum(vec_start_mid[i] * vec_start_end[i] for i in range(3))
    norm_vec_start2end = sum(vec_start_end[i] ** 2 for i in range(3))

    if norm_vec_start2end == 0:
        print('Start and End points are the same one!')
        return 0#some instance we have object stay at one point for some time
        #exit()

    # project_ratio = |start-mid| cos(\theta) / |start-end|
    project_ratio = dot_product_start2mid_start2end / norm_vec_start2end

    # If project_ratio > 1, mid_point is outside the start-end line segment and the nearest point is simply p2
    # If project_ratio < 0, mid_point is outside the start-end line segment and the nearest point is simply p1
    project_ratio = max(0, min(1, project_ratio))

    projected_x = start_x + project_ratio * vec_start_end[0]
    projected_y = start_y + project_ratio * vec_start_end[1]
    projected_z = start_z + project_ratio * vec_start_end[2]

    return math.sqrt((projected_x - mid_x)**2 + (projected_y - mid_y)**2 + (projected_z - mid_z)**2)


def synchronized_euclidean_distance(start_point: Point, mid_point: Point, end_point: Point) -> float:
    """
    Step 1: Project mid_point to the line start_point - end_point based on Time Stamps
    Step 2: Calculate the Euclidean distance
    Note: The distance calculation is based on x-y-z Cartesian coordinate system --
          Please check Point.latlon2cartesian() before calling this function

                                  o (mid_point)
                                 /
                                /
        (start_point) o ------o------ o (end_point)
                               p' (based on time)
    """
    start_x, start_y, start_z = start_point.get_cx(), start_point.get_cy(), start_point.get_cz()
    end_x, end_y, end_z = end_point.get_cx(), end_point.get_cy(), end_point.get_cz()
    mid_x, mid_y, mid_z = mid_point.get_cx(), mid_point.get_cy(), mid_point.get_cz()

    if any(val is None for val in [start_x, start_y, start_z, end_x, end_y, end_z, mid_x, mid_y, mid_z]):
        print("Distance calculation needs coordinate coversion from lat/lon to Cartesian one")
        exit()

    start_t, end_t, mid_t = start_point.get_time(), end_point.get_time(), mid_point.get_time()

    if start_t is None or end_t is None or mid_t is None:
        print('Time stamp is missing from input!')
        exit()

    if start_t == end_t:
        return 0

    if start_t <= mid_t <= end_t:

        project_ratio = (mid_t - start_t) / (end_t - start_t)

        projected_x = start_x + project_ratio * (end_x - start_x)
        projected_y = start_y + project_ratio * (end_y - start_y)
        projected_z = start_z + project_ratio * (end_z - start_z)

        return math.sqrt((projected_x - mid_x) ** 2 + (projected_y - mid_y) ** 2 + (projected_z - mid_z) ** 2)
    else:
        print("Please check the time stamps of input!")
        print('start_point',start_point.get_x(),mid_point.get_x(),end_point.get_x())
        exit()


def haversine_distance(p1: Point, p2: Point) -> float:
    """
    https://www.movable-type.co.uk/scripts/latlong.html
    Given pairs of lat/lon position, return the distance based on Haversine formula
    """
    earth_r = 6371010
    degree2radian = math.pi / 180  # Assume the given lat/lon is in degree, while the cos/sin requires radian

    lat1, lon1 = p1.get_y(), p1.get_x()
    lat2, lon2 = p2.get_y(), p2.get_x()

    diff_lat, diff_lon = lat2 - lat1, lon2 - lon1

    a = (math.sin(diff_lat * degree2radian / 2))**2 + \
        math.cos(lat1 * degree2radian) * math.cos(lat2 * degree2radian) * ((math.sin(diff_lon * degree2radian / 2))**2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return earth_r * c






