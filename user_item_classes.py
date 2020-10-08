# Overview program to piece together functions needed for the project

# Project: Object location tracking for memory impaired users
# Outline:	- System tracks locations of objects using computer vision
#			- If the object is misplaced, the system will help to find it
#
# Operation:
#			- Specify item to track
#			- Item location is updated if it is in view of the camera
#			- Item designated as lost
#			- System will give directions to last location object was seen
#			- Prompts user to check pockets/bag as camera cannot see these
#			
# Wearable systems for elderly
# Market need for the idea
# Set up/scanning object could be very complicated for elderly

# Need to prove that idea works - does not need to be a finished idea
# Demonstrate that idea is important and usable - there needs to be a market
# Important for the user and useful for the user
# Think about usability - is useful but isn't annoying to use otherwise
#						they will stop using it

# Usability, actual use, affordability

###############################################################################

# User class
class User():
	"""The user of the object locating program."""
	def __init__(self, name):
		"""The user has a name and a location.
		Default location is at [0,0]."""
		self.name = name
		self.location = [0,0]

	def get_name(self):
		"""Return the name of the user."""
		return self.name

	def get_location(self):
		"""Return the location of the user."""
		return [self.location[0], self.location[1]]

	def update_location(self, new_location):
		"""Update the location of the user."""
		self.location = new_location

	def move_pos_x(self):
		"""Move the user in the positive x direction."""
		self.location[0] += 1

	def move_pos_y(self):
		"""Move the user in the positive y direction."""
		self.location[1] += 1

	def move_neg_x(self):
		"""Move the user in the positive x direction."""
		self.location[0] -= 1

	def move_neg_y(self):
		"""Move the user in the positive y direction."""
		self.location[1] -= 1

# Item class
class Item():
	"""An item that exists in the world."""
	def __init__(self, name):
		"""Every item has a name, location, visibility status and lost status.
		Default location is at [0,0]."""
		self.name = name
		self.location = [0,0]
		self.visible = False
		self.lost = False

	def get_name(self):
		"""Return the name of the object."""
		return self.name

	def get_location(self):
		"""Return the location of the object."""
		return [self.location[0], self.location[1]]

	def update_location(self, new_location):
		"""Update the location of the object."""
		self.location = new_location

	def check_visibility(self):
		"""Check if item is visible to user."""
		return self.visible

	def update_visibility(self, visibility):
		"""Update the visibility of the item."""
		self.visible = visibility