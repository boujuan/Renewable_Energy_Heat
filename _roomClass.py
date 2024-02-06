import matplotlib.pyplot as plt

class Room:
    def __init__(self, room_dimensions, floor_material, wall_material, ceiling_material, 
                 floor_thickness, wall_thickness, ceiling_thickness, desired_temp):
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
        heat_demand = heat_transfer_coeff * insulator_area * delta_temperature # Q = U * A * deltaT
        return heat_demand

    def total_power_demand(self, outside_temp): # outside_temp is a new external parameter
        hpd_walls = self._heat_power_demand(self.structure["Wall"][0], self.structure["Wall"][1],
                                            self._walls_area(), outside_temp)
        hpd_floor = self._heat_power_demand(self.structure["Floor"][0], self.structure["Floor"][1],
                                            self._floor_area(), outside_temp)
        hpd_ceiling = self._heat_power_demand(self.structure["Ceiling"][0], self.structure["Ceiling"][1],
                                              self._floor_area(), outside_temp)
        return hpd_walls + hpd_floor + hpd_ceiling

class ClimateData:
    def __init__(self, average_temperatures):
        self.months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.average_temperatures = average_temperatures # in Celsius
        self.average_yearly_temp = sum(self.average_temperatures) / len(self.average_temperatures)

    def calculate_yearly_cooling_demand(self, room):
        heating_demand = []
        for avg_temp in self.average_temperatures:
            outside_temp = avg_temp + 273.15 # Convert to Kelvin
            heating_demand.append(abs(room.total_power_demand(outside_temp)))
        return heating_demand

class Plotter:
    @staticmethod
    def plot_cooling_demand(months, cooling_demand, average_temperatures):
        fig, ax1 = plt.subplots()

        # Plot heating demand as bar chart with blue color
        ax1.bar(months, cooling_demand, color='tab:blue')
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
        plt.grid()
        plt.savefig('figures/monthly_cooling_demand.png')
        plt.show()