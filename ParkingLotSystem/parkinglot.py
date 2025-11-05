import datetime

class ParkingLot:
    def __init__(self, name):
        self.name =  name
        self.floors = []
        self.entry_gates = []
        self.exit_gates = []
         
    def add_floor(self, floor):
        self.floors.append(floor)
    
    def get_available_spot(self, vehicle_type):
        for floor in self.floors:
            slot = floor.get_available_spot(vehicle_type)
            if slot:
                return slot
        return None
    
    def update_display(self):
        free_cars = sum(spot.is_free for spot in self.car_spots)
        free_bikes = sum(spot.is_free for spot in self.bike_spots)
        self.display_board.update("Car", free_cars)
        self.display_board.update("Bike", free_bikes)
        self.display_board.show()
    
    
class ParkingFloor:
    def __init__(self, number):
        self.number = number
        self.spots = []
        self.display_board = DisplayBoard()
        
    def add_spot(self, spot):
        spot.floor = self
        self.spots.append(spot)
        self.display_board.update_count(spot.type, +1)
        
    def get_available_spot(self, vehicle_type):
        for spot in self.spots:
            if spot.is_available and spot.type == vehicle_type:
                return spot
        return None
    
    def occupy_spot(self, spot):
        spot.is_available = False
        self.display_board.update_count(spot.type, -1)
        
    def free_spot(self, spot):
        spot.is_available = True
        self.display_board.update_count(spot.type, +1)
    

class ParkingSpot:
    def __init__(self, spot_id, spot_type, floor=None) -> None:
        self.id = spot_id
        self.type = spot_type
        self.is_available = True
        self.vehicle = None
        self.floor = floor
        
    def assign_vehicle(self, vehicle):
        self.vehicle = vehicle
        self.is_available = False
        
    def remove_vehicle(self):
        self.vehicle = None
        self.is_available = True
    
    def get_rate(self):
        if self.type == "CAR":
            return 50
        elif self.type == "BIKE":
            return 20
        else:
            return 100
        
        
class Vehicle:
    def __init__(self, license_number, vehicle_type) -> None:
        self.license_number = license_number
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
        self.amount = max(10, duration * self.spot.get_rate())

    

class EntranceGate:
    def __init__(self, gate_id, parking_lot):
        self.gate_id = gate_id
        self.parking_lot = parking_lot

    def issue_ticket(self, vehicle):
        spot = self.parking_lot.get_available_spot(vehicle.vehicle_type)
        if not spot:
            print("No available spot for", vehicle.vehicle_type)
            return None
        spot.assign_vehicle(vehicle)
        ticket = Ticket(f"T-{vehicle.license_number}", vehicle, spot)
        spot.floor.occupy_spot(spot)
        print(f"Ticket issued: {ticket.ticket_id}")
        spot.floor.display_board.show_status()
        return ticket



class ExitGate:
    def __init__(self, gate_id):
        self.gate_id = gate_id

    def process_exit(self, ticket):
        ticket.close_ticket()
        spot = ticket.spot
        spot.remove_vehicle()
        spot.floor.free_spot(spot)
        print(f"Ticket closed. Amount: ₹{ticket.amount:.2f}")
        spot.floor.display_board.show_status()

class DisplayBoard:
    def __init__(self):
        # Keeps count of available slots per vehicle type
        self.available_spots = {
            "CAR": 0,
            "BIKE": 0,
            "TRUCK": 0
        }

    def update_count(self, vehicle_type, delta):
        # delta = +1 (spot freed), -1 (spot occupied)
        if vehicle_type in self.available_spots:
            self.available_spots[vehicle_type] += delta

    def show_status(self):
        print("---- Display Board ----")
        for vehicle_type, count in self.available_spots.items():
            print(f"{vehicle_type}: {count} spots available")
        print("------------------------\n")



if __name__ == "__main__":
    # Create parking lot and floors
    lot = ParkingLot("TechPark Parking")
    floor1 = ParkingFloor(1)
    floor2 = ParkingFloor(2)
    lot.add_floor(floor1)
    lot.add_floor(floor2)

    # Add some parking spots
    for i in range(2):
        floor1.add_spot(ParkingSpot(f"F1S{i}", "CAR"))
        floor2.add_spot(ParkingSpot(f"F2S{i}", "CAR"))

    # Create gates
    entry_gate = EntranceGate(1, lot)
    exit_gate = ExitGate(1)

    # Vehicles arrive
    car1 = Car("KA01AB1234")
    car2 = Car("KA01AB5678")

    ticket1 = entry_gate.issue_ticket(car1)
    ticket2 = entry_gate.issue_ticket(car2)

    # Vehicle exits
    exit_gate.process_exit(ticket1)
    exit_gate.process_exit(ticket2)
    print(floor1.display_board.show_status())
    print(floor2.display_board.show_status())