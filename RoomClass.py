import matplotlib.pyplot as plt

class Room:
    def __init__(self, room_dimensions, floor_material, wall_material, ceiling_material, floor_thickness, wall_thickness, ceiling_thickness, desired_temp):
        self.room_size = room_dimensions # [length, width, height] in meters
        self.desired_temp = desired_temp + 273.15
        self.materials = {"Polyurethane foam": 0.022, # heat transfer coefficient [W/mK]
                          "Concrete": 0.11}
        self.structure = {"Wall": [self.materials[wall_material], wall_thickness/10], # Heat transfer coefficient, Convert cm to m
                          "Floor": [self.materials[floor_material], floor_thickness/10],
                          "Ceiling": [self.materials[ceiling_material], ceiling_thickness/10]}

    def _walls_area(self):
        return self.room_size[0]*self.room_size[2]*2 + self.room_size[1]*self.room_size[2]

    def _floor_area(self):
        return self.room_size[0]*self.room_size[1]

    def _total_surface_area(self): # Unused method
        return self._walls_area() + self._floor_area()*2

    def _heat_power_demand(self, material, thickness, insulator_area, outside_temp):
        heat_transfer_coeff = material / thickness # U = k/L
        delta_temperature = self.desired_temp - outside_temp
        heat_demand = heat_transfer_coeff * insulator_area * delta_temperature
        return heat_demand

    def total_power_demand(self, outside_temp): # outside_temp is a new external parameter
        hpd_walls = self._heat_power_demand(self.wall_material, self.wall_thickness/100, self._walls_area(), outside_temp) # FIX THICKNESS
        hpd_floor = self._heat_power_demand(self.floor_material, self.floor_thickness/100, self._floor_area(), outside_temp)
        hpd_ceiling = self._heat_power_demand(self.ceiling_material, self.ceiling_thickness/100, self._floor_area(), outside_temp)
        return hpd_walls + hpd_floor + hpd_ceiling

class ClimateData:
    def __init__(self, average_temperatures):
        self.months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.average_temperatures = average_temperatures

    def calculate_yearly_heating_demand(self, room):
        heating_demand = []
        for avg_temp in self.average_temperatures:
            outside_temp = avg_temp + 273.15 # Convert to Kelvin
            heating_demand.append(abs(room.total_power_demand(outside_temp)))
        return heating_demand

class Plotter:
    @staticmethod
    def plot_data(months, heating_demand, average_temperatures):
        # Create figure and axis objects
        fig, ax1 = plt.subplots()

        # Plot heating demand as bar chart with blue color
        ax1.bar(months, heating_demand, color='tab:blue')
        ax1.set_xlabel('Months')
        ax1.set_ylabel('Cooling Demand (kW)', color='tab:blue')
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        # Create a twin axis for average temperature
        ax2 = ax1.twinx()

        # Plot average temperature as line graph with red color
        ax2.plot(months, average_temperatures, marker='o', color='tab:red')
        ax2.set_ylabel('Average Temperature (°C)', color='tab:red')
        ax2.tick_params(axis='y', labelcolor='tab:red')

        # Set title and display the plot
        plt.title('Monthly cooling demand and average monthly temperatures in Hamburg')
        plt.show()

if __name__ == "__main__":
    average_temperature_hamburg = [1.7, 2, 4.5, 9.1, 13.3, 16.3, 18.5, 18.1, 14.9, 10.5, 6, 3] # in °C
    coldroom_dimensions = [5, 5, 3] # in meters
    desired_fridge_temperature = 8 # in °C
    
    # Create a room object with dimensions [x, y, z] in meters, materials for floor, wall, and ceiling, thickness in cm and desired temperature in °C
    coldRoom = Room(coldroom_dimensions, "Concrete", "Polyurethane foam", "Polyurethane foam", 50, 15, 20, desired_fridge_temperature)    
    hamburg = ClimateData(average_temperature_hamburg)
    
    heating_demand = hamburg.calculate_yearly_heating_demand(coldRoom)

    Plotter.plot_data(hamburg.months, heating_demand, average_temperature_hamburg)