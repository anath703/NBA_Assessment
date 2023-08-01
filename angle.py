import pandas as pd
import numpy as np
import math


df =pd.read_excel('Data.xlsx')

# Hoop coordinates
hoop_x, hoop_y = 41.5,0

degrees_bool= True

# general function to calculate the angle
def calculate_angle(x1, y1, x2, y2, degrees=False):
    x = x2 - x1
    y = y2 - y1
    rads = np.arctan2(y, x)
    if degrees:
        return np.degrees(rads)
    else:
        return rads

# function to calculate the angle to the hoop
def calculate_angle_to_hoop(row, degrees=False):
    return calculate_angle(row['x_smooth'], row['y_smooth'], hoop_x, hoop_y, degrees)

# function to calculate the angle to the ball
def calculate_angle_to_ball(row, degrees=False):
 #   if row['type'] == 'ball':
  #      return None  # return None for the ball itself
  #  else:
        # get the row for the ball at the same possession and frame
        ball_row = df[(df['type'] == 'ball') & 
                      (df['possessionId'] == row['possessionId']) & 
                      (df['frame'] == row['frame'])].iloc[0]
        return calculate_angle(row['x_smooth'], row['y_smooth'], ball_row['x_smooth'], ball_row['y_smooth'], degrees)


def calculate_angle_between_players(df, degrees=False):
    # Initialize a DataFrame to store the angles
    angles_df = pd.DataFrame(index=df.index, columns=df.index)

    # Calculate the angle for each pair of players
    for i in df.index:
        for j in df.index:
            if i != j:  # no need to calculate the angle between a player and themselves
                angles_df.loc[i, j] = calculate_angle(df.loc[i, 'x_smooth'], df.loc[i, 'y_smooth'],
                                                      df.loc[j, 'x_smooth'], df.loc[j, 'y_smooth'], 
                                                      degrees=degrees)

    return angles_df



# add 'angle_to_hoop' column to dataframe
df['angle_to_hoop'] = df.apply(calculate_angle_to_hoop, args=(degrees_bool,), axis=1)

# add 'angle_to_ball' column to dataframe
df['angle_to_ball'] = df.apply(calculate_angle_to_ball, args=(degrees_bool,), axis=1)

# Calculate the angles between each player
angles_df = calculate_angle_between_players(df, degrees_bool)




# import matplotlib.pyplot as plt

# def plot_frame(play):
#     # Split players into home and away
#     home_positions = play[play['type'] == 'home']
#     away_positions = play[play['type'] == 'away']

#     # Create scatter plots for home and away player positions
#     plt.scatter(home_positions['x_smooth'], home_positions['y_smooth'], c='blue', label='Home Players')
#     plt.scatter(away_positions['x_smooth'], away_positions['y_smooth'], c='green', label='Away Players')
    
#     # Create a scatter plot for ball position
#     ball_position = play[play['type'] == 'ball']
#     plt.scatter(ball_position['x_smooth'], ball_position['y_smooth'], c='red', label='Ball')

#     # Label each player by their index, angle to hoop, and angle to ball
#     for idx, row in play.iterrows():
#         label = f"{idx}, {row['angle_to_hoop']:.2f}, {row['angle_to_ball']:.2f}"
#         plt.text(row['x_smooth'], row['y_smooth'], label)


#     # Display hoop position
#     plt.scatter(hoop_x, hoop_y, c='orange', marker='o', label='Hoop')

#     # Setting the limit for x and y axis
#     plt.xlim(0, 47)
#     plt.ylim(-25, 25)
    
#     plt.title('Player and Ball Positions')
#     plt.xlabel('x_smooth')
#     plt.ylabel('y_smooth')
#     plt.legend(loc='upper left')
#     plt.grid(True)
#     plt.show()

# # Call the function
# plot_frame(df)
