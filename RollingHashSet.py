import hashlib

class RollingHashSet:
  def __init__(self, max_size):
    # Set the maximum size of the hash set
    self.max_size = max_size
    # Initialize the hash set with an empty list
    self.items = []

  def add(self, item):
    # Hash the item
    item_hash = hashlib.sha1(item.encode()).hexdigest()
    # Add the item to the beginning of the list
    self.items.insert(0, item_hash)
    # If the list is larger than the maximum size, remove the oldest item
    if len(self.items) > self.max_size:
      self.items.pop()

  def __contains__(self, item):
    # Hash the item
    item_hash = hashlib.sha1(item.encode()).hexdigest()

    # Return True if the item is in the list, False otherwise
    return item_hash in self.items
