import _roomClass as rc

def calculate_heating_demand(hamburg, coldRoom):    
    heating_demand = hamburg.calculate_yearly_heating_demand(coldRoom)
    for month, demand in zip(hamburg.months, heating_demand):
        print(f"Heating demand in {month}: {demand:.2f} kW")
    rc.Plotter.plot_heating_demand(hamburg.months, heating_demand, hamburg.average_temperatures)
    return heating_demand

def calculate_cop(qout, compressor_power):
    return qout / compressor_power

def seasonal_cop(heating_demand, compressor_power):
    seasonal_cop = []
    for qout in heating_demand:
        seasonal_cop.append(calculate_cop(qout, compressor_power))
    return seasonal_cop

def plot_seasonal_cop(months, seasonal_cop):
    fig, ax1 = rc.plt.subplots()
    ax1.bar(months, seasonal_cop, color='tab:blue')
    ax1.set_xlabel('Months')
    ax1.set_ylabel('Seasonal COP', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    rc.plt.show()
    


if __name__ == "__main__":
    average_temperature_hamburg = [1.7, 2, 4.5, 9.1, 13.3, 16.3, 18.5, 18.1, 14.9, 10.5, 6, 3] # in °C [Source: https://en.climate-data.org/europe/germany/hamburg/hamburg-69/]
    desired_freezer_temperature = -18 # in °C
    coldroom_dimensions = [4, 3, 2] # in meters
    floor_material = "Concrete"
    wall_material = "Polyurethane foam"
    ceiling_material = "Polyurethane foam"
    compressor_power = 10 # in kW
    
    # Create a cold room and climate data objects for location
    coldRoom = rc.Room(coldroom_dimensions, floor_material, wall_material, ceiling_material, 50, 15, 20, desired_freezer_temperature)    
    hamburg = rc.ClimateData(average_temperature_hamburg)

    yearly_heating_demand = calculate_heating_demand(hamburg, coldRoom)
    seasonal_cop = seasonal_cop(yearly_heating_demand, compressor_power)
    
    for month, cop in zip(hamburg.months, seasonal_cop):
        print(f"Seasonal COP in {month}: {cop:.2f}")
    
    plot_seasonal_cop(hamburg.months, seasonal_cop)