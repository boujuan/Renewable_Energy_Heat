import matplotlib.pyplot as plt
import numpy as np

class Room:
    def __init__(self, room_dimensions, floor_material, wall_material, ceiling_material, 
                 floor_thickness, wall_thickness, ceiling_thickness, desired_temp):
        self.room_size = room_dimensions # [length, width, height] in meters
        self.desired_temp = desired_temp + 273.15 # Convert to Kelvin
        self.materials = {"Polyurethane foam": 0.022,
                          "Extruded Polystyrene lowest": 0.025,
                          "Extruded Polystyrene highest": 0.040,
                          "Cellular Glass lowest": 0.038,
                          "Cellular Glass highest": 0.055,
                          "Polyurethane lowest": 0.022,
                          "Polyurethane highest": 0.035,
                          "Concrete": 0.11}
        self.structure = {"Wall": [self.materials[wall_material], wall_thickness/100], # Heat transfer coefficient, Convert cm to m
                          "Floor": [self.materials[floor_material], floor_thickness/100],
                          "Ceiling": [self.materials[ceiling_material], ceiling_thickness/100]}

    def _walls_area(self):
        return self.room_size[0]*self.room_size[2]*2 + self.room_size[1]*self.room_size[2]*2 # in m^2

    def _floor_area(self):
        return self.room_size[0]*self.room_size[1] # in m^2

    def _total_surface_area(self):
        return self._walls_area() + self._floor_area()*2 # in m^2

    def _heat_power_demand(self, material, thickness, insulator_area, outside_temp):
        heat_transfer_coeff = material / thickness # U [W/m^2K] = k[W/mK]/L[m]
        delta_temperature = self.desired_temp - outside_temp # [K]
        heat_demand = heat_transfer_coeff * insulator_area * delta_temperature # Q [W] = U [W/m^2K] * A [m^2] * deltaT [K]
        return heat_demand # in Watts

    def total_power_demand(self, outside_temp): # outside_temp is a new external parameter
        hpd_walls = self._heat_power_demand(self.structure["Wall"][0], self.structure["Wall"][1],
                                            self._walls_area(), outside_temp)
        hpd_floor = self._heat_power_demand(self.structure["Floor"][0], self.structure["Floor"][1],
                                            self._floor_area(), outside_temp)
        hpd_ceiling = self._heat_power_demand(self.structure["Ceiling"][0], self.structure["Ceiling"][1],
                                              self._floor_area(), outside_temp)
        return hpd_walls + hpd_floor + hpd_ceiling # in Watts

class ClimateData:
    def __init__(self, average_temperatures):
        self.months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.average_temperatures = average_temperatures # in Celsius
        self.average_yearly_temp = sum(self.average_temperatures) / len(self.average_temperatures)

    def calculate_yearly_cooling_demand(self, room):
        cooling_demand = []
        for avg_temp in self.average_temperatures:
            outside_temp = avg_temp + 273.15 # Convert to Kelvin
            cooling_demand.append(abs(room.total_power_demand(outside_temp)))
        return cooling_demand # in Watts

class Plotter:
    @staticmethod
    def plot_cooling_demand(months, cooling_demand, average_temperatures):
        fig, ax1 = plt.subplots()

        # Plot heating demand as bar chart with blue color
        ax1.bar(months, cooling_demand, color='tab:blue')
        ax1.set_xlabel('Months')
        ax1.set_ylabel('Cooling Demand (W)', color='tab:blue')
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        # Create a twin axis for average temperature
        ax2 = ax1.twinx()
        
        # Calculate the average yearly temperature
        avg_yearly_temp = np.mean(average_temperatures)
        print(f'Average yearly temperature: {avg_yearly_temp:.2f}°C')

        # Plot average temperature as line graph with red color
        ax2.plot(months, average_temperatures, marker='o', color='tab:red')
        # Plot the average yearly temperature as a line graph
        ax2.axhline(avg_yearly_temp, color='black', linestyle='--', label='Average yearly temperature')
        
        ax2.set_ylabel('Avg. Temperature (°C)', color='tab:red')
        ax2.tick_params(axis='y', labelcolor='tab:red')

        # Set title and display the plot
        plt.title('Monthly cooling demand and average monthly temperatures in Hamburg')
        plt.legend()
        plt.grid()
        plt.savefig('figures/monthly_cooling_demand.png', dpi=300, transparent=True)
    
    @staticmethod
    def plot_temperature_duration_curve(temperatures):
        sorted_temperatures = sorted(temperatures, reverse=True)
        duration = range(1, len(sorted_temperatures) + 1)
        
        # 3rd degree fitting polynomial
        coefficients = np.polyfit(duration, sorted_temperatures, 3)
        polynomial = np.poly1d(coefficients)
        fitted_temperatures = polynomial(duration)
        
        plt.plot(duration, fitted_temperatures)
        plt.xlabel('Duration (months)')
        plt.ylabel('Temperature (°C)')
        plt.title('Temperature Duration Curve Hamburg')
        plt.grid(True)
        plt.savefig('figures/temperature_duration_curve.png', dpi=300, transparent=True)