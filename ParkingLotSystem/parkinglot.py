import datetime

class ParkingLot:
    def __init__(self, name):
        self.name =  name
        self.floors = []
        self.entry_gates = []
        self.exit_gates = []
         
    def add_floor(self, floor):
        self.floors.append(floor)
    
    def get_available_slot(self, vehicle_type):
        for floor in self.floors:
            slot = floor.get_available_slot(vehicle_type)
            if slot:
                return slot
        return None
    
    
class ParkingFloor:
    def __init__(self, number):
        self.number = number
        self.spots = []
        self.display_board = DisplayBoard()
        
    def add_spot(self,spot):
        self.spots.append(spot)
        
    def get_available_spot(self, vehicle_type):
        for spot in self.spots:
            if spot.is_available and spot.type == vehicle_type:
                return spot
        return None
    
    
class ParkingSpot:
    def __init__(self, spot_id, spot_type) -> None:
        self.id = spot_id
        self.type = spot_type
        self.is_available = True
        self.vehicle = None
        
    def assign_vehicle(self, vehicle):
        self.vehicle = vehicle
        self.is_available = False
        
    def remove_vehicle(self):
        self.vehicle = None
        self.is_available = True
        
        
class Vehicle:
    def __init__(self, license_number, vehicle_type) -> None:
        self.lincense_number = license_number
        self.vehicle_type = vehicle_type
        
class Car(Vehicle):
    def __init__(self, license_number) -> None:
        super().__init__(license_number, "CAR")
        

class Ticket:
    def __init__(self, ticket_id, vehicle, spot):
        self.ticket_id = ticket_id
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = datetime.datetime.now()
        self.exit_time = None
        self.amount = 0

    def close_ticket(self):
        self.exit_time = datetime.datetime.now()
        duration = (self.exit_time - self.entry_time).seconds / 3600
        self.amount = duration * self.spot.get_rate()

    

class EntranceGate:
    def __init__(self, gate_id, parking_lot):
        self.gate_id = gate_id
        self.parking_lot = parking_lot

    def issue_ticket(self, vehicle):
        spot = self.parking_lot.get_available_slot(vehicle.vehicle_type)
        if not spot:
            return None
        spot.assign_vehicle(vehicle)
        ticket = Ticket(f"T-{vehicle.license_number}", vehicle, spot)
        return ticket


class ExitGate:
    def __init__(self, gate_id):
        self.gate_id = gate_id

    def process_exit(self, ticket):
        ticket.close_ticket()
        ticket.spot.remove_vehicle()
        return ticket.amount
