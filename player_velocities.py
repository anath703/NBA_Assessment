import pandas as pd
import numpy as np
import math


df =pd.read_excel('Data.xlsx')

# df.loc[0,'x_smooth']= 2
# df.loc[0,'y_smooth']= 2

# df.loc[0,'x_vel']= 1
# df.loc[0,'y_vel']= -1

# df.loc[1,'x_smooth']= 3
# df.loc[1,'y_smooth']= -1

# df.loc[1,'x_vel']= 1
# df.loc[1,'y_vel']= 1

degrees_bool= True

def perp( a ) :
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

# line segment a given by endpoints a1, a2
# line segment b given by endpoints b1, b2
# https://web.archive.org/web/20111108065352/https://www.cs.mun.ca/%7Erod/2500/notes/numpy-arrays/numpy-arrays.html

def seg_intersect(a1, a2, b1, b2):
    da = a2 - a1
    db = b2 - b1
    dp = a1 - b1
    dap = perp(da)

    # Check if vectors are parallel
    cross_product = np.cross(da, db)
    if np.allclose(cross_product, 0):
        return None  # Return None if vectors are parallel

    denom = np.dot(dap, db)
    num = np.dot(dap, dp)

    # check if denom is very close to zero (which would lead to division by zero)
    if abs(denom) < 1e-6:
        return None

    return (num / denom.astype(float)) * db + b1

def calculate_angle(a, b, c, degrees=True):
    #https://manivannan-ai.medium.com/find-the-angle-between-three-points-from-2d-using-python-348c513e2cd
    """Calculate the angle between vectors `ba` and `bc`."""
    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    return np.degrees(angle) if degrees else angle  # return angle in degrees or radians

def get_angle_and_intersection(row1, row2, degrees=True):
    # current position
    a1 = np.array([row1['x_smooth'], row1['y_smooth']])
    # current position + velocity vector
    a2 = a1 + np.array([row1['x_vel'], row1['y_vel']])
    b1 = np.array([row2['x_smooth'], row2['y_smooth']])
    b2 = b1 + np.array([row2['x_vel'], row2['y_vel']])
    intersection = seg_intersect(a1, a2, b1, b2)
    if intersection is not None:  # calculate angle only if intersection exists
        angle = calculate_angle(a1, intersection, b1, degrees=degrees)
        return angle, intersection

# Get DataFrames with player indices as both columns and index
angle_df = pd.DataFrame(index=df.index, columns=df.index)
intersection_df = pd.DataFrame(index=df.index, columns=df.index)

# Calculate angle and intersection for each pair of players
for i in df.index:
    for j in df.index:
        if i != j:  # no need to calculate self-angle and self-intersection
            result = get_angle_and_intersection(df.loc[i], df.loc[j], degrees= degrees_bool)
            if result is not None:
                angle, intersection = result
                angle_df.loc[i, j] = angle
                intersection_df.loc[i, j] = intersection
