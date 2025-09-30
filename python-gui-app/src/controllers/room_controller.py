class RoomController:
    def __init__(self):
        self.rooms = []

    def create_room(self, room_name):
        if room_name and room_name not in self.rooms:
            self.rooms.append(room_name)
            return True
        return False

    def enter_room(self, room_name):
        if room_name in self.rooms:
            return True
        return False

    def list_rooms(self):
        return self.rooms.copy()