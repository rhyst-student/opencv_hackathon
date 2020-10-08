import user_item_classes as ov
import cv2
import time

## Theoretical main loop
# Initialise everything
# list_items = items to be tracked in system
# Specify items to track


def setup_user():
    """Set up and initialise user."""
    # Initialise user
    user = ov.User("Rhys")

    return user

def setup_tracked_items(items):
    """Set up and initialise items to be tracked."""
    # List of tracked Item objects
    tracking_items = []
    # Initialise all items being tracked to a tracking list
    for i in range(len(list_items)):
        tracking_items.append(ov.Item(list_items[i]))
    return tracking_items

# change "iteration" to the list from the camera feed
def get_visible_items(camera_frame_list):
    """Gets visible items from camera feed.
    Change the list values for the simulation."""
    items = [camera_frame_list] # -- list from camera feed

    # For simulation set phone visible for first two iterations, then
    # not visible so it can be set as lost and found.
    # for item in tracking_items:
    #   if iteration == 1 and item.name == "phone":
    #       item.visible = True
    #   elif iteration == 2 and item.name == "phone":
    #       item.visible = True
    #   elif iteration == 3 and item.name == "phone":
    #       item.visible = False
    # items = ["phone"]

    return items

def update_item_visibility():
    """Set items visible depending on iteration."""
    for item in tracking_items:
    # Make item visible if on camera feed
        if item.name in camera_items:
            item.visible = True
        else:
            item.visible = False

# Set in simulation - increment x-position
def update_user_location(user):
    """Update user location from IMU/GPS, but manually with this function
    for the simulation."""
    # user.move_pos_x()

def update_item_locations():
    for item in tracking_items:
        # Check if item visible
        if item.visible == True:
            item.update_location(user.get_location())
            # item.location = user.get_location()
        else:
            # print(f"{item.name}: HEY HI HOW ARE YA {item.location} {item.visible}")
            continue

def print_user_location(user):
    """Print location of user."""
    print(f"{user.name.title()}: {user.location}")

def print_all_item_locations():
    """Print location of all items."""
    for item in tracking_items:
        if item.visible == True:
            visible_word = "visible"
        else:
            visible_word = "not visible"

        if item.lost == True:
            lost_word = "lost"
        else:
            lost_word = "not lost"

        print(f"{item.name.title()}: {item.get_location()}, {visible_word}, {lost_word}.")

def move_user(user):
    user.move_pos_x()

def find_lost_item(item):
    if item.lost == True:
        print(f"{item.name.title()} is lost. Check your pockets and bag!")
        print(f"Otherwise, it is at {item.location}.")

        while(True):
            found_confirmation = input(f"When {item.name} is found, press 'y'. ")
            if found_confirmation == 'y':
                item.lost = False
                break
            else:
                continue

####################################




#################################3
# Program

# Initialise user and items
user = setup_user()
list_items = []
while(True):
    track_item = input("What item would you like to track? ('q' to end input) ")
    if track_item == 'q':
        break
    else:
        list_items.append(track_item)

tracking_items = setup_tracked_items(list_items)

# Simulation iteration (runs 4 iterations)
iteration = 0

while(1):
    # Get visible items
    ## TODO - put camera feed in here, one frame at a time
    # camera_items = get_visible_items(camera_frame_list)

    # Update item visibility
    # update_item_visibility()

    # Update user location and print
    update_user_location(user)

    # Update item locations and print
    update_item_locations()

    # Print location of user and items
    print_user_location(user)
    print_all_item_locations()
    print()

    # # Update lost status
    # lost_item(i)

    # # Find any lost items
    # find_lost_items()

    

    

    # Wait for key press for next frame
    while(True):
        next_frame = input("Next frame (n), Quit (q), Lost item(i)")
        if next_frame == 'q':
            exit()
        elif next_frame == 'n':
            #### TODO - fix this to update the visibility and lost status for each frame
            for item in tracking_items:
                if (item.name == 'phone'):
                    if iteration < 3:
                        item.visible = True
                    else:
                        item.visible = False
                #     item.visible = True
                # elif item.name == 'phone' and iteration >= 3:
                #     item.visible = False
                        item.lost = True
                elif item.name == 'wallet':
                    if iteration > 2 and iteration < 4:
                        item.visible = True
                    else:
                        item.visible = False
            break
        elif next_frame == 'i':
            lost_item = input("What item is lost? ")
            for item in tracking_items:
                if lost_item == item.name:
                    find_lost_item(item)
                    user.update_location(item.get_location())
                    break
                else:
                    print(f"{lost_item} not lost.")
                    break
        else:
            continue
    
    # Move the user some distance
    move_user(user)

    iteration += 1
    print(iteration)

#############################################################






#### ignore these functions
# def find_lost_items():
#   for item in tracking_items:
#       # Check if item is lost
#       if item.lost == True:
#           print(f"{item.name} is lost. Check your pockets and bag.")
#           print(f"If {item.name} is not there, check at {item.location}.")

# def lost_item(iteration):
#   """Declare an item as lost"""
#   for item in tracking_items:
#       if iteration == 3 and item == "phone":
#           item.lost = True


# # -- Testing functions

# def visible_item_locations():
#   """Print location of visible items."""
#   for item in tracking_items:
#       if item.visible == True:
#           print(f"{item.name} is at {item.location}.")

# def lost_item_locations():
#   """Print location of lost items."""
#   for item in tracking_items:
#       if item.lost == True:
#           print(f"{item.name} is LOST. Look at {item.location}.")



# def item_status():
#   """Print status of each item."""
#   print(f"tracking: {list_items}")
#   print(f"visible: {camera_items}")

# def set_item_lost(item):
#   """Set the item as lost."""
#   item.lost = True

# def set_item_location(item, location):
#   item.location = location

# def set_item_visible(item, visibility=True):
#   if visibility == False:
#       item.visible = False

# def set_item_lost(item, lost=True):
#   if lost == False:
#       item.lost = False

# def move_user(user):
#   """Move the user some coordinates."""