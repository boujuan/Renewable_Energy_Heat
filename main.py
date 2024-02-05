import _roomClass as rc

if __name__ == "__main__":
    average_temperature_hamburg = [1.7, 2, 4.5, 9.1, 13.3, 16.3, 18.5, 18.1, 14.9, 10.5, 6, 3] # in °C [Source: https://en.climate-data.org/europe/germany/hamburg/hamburg-69/]
    desired_freezer_temperature = -18 # in °C
    coldroom_dimensions = [4, 3, 2] # in meters
    floor_material = "Concrete"
    wall_material = "Polyurethane foam"
    ceiling_material = "Polyurethane foam"

    # Create a cold room and climate data objects for location
    coldRoom = rc.Room(coldroom_dimensions, floor_material, wall_material, ceiling_material, 50, 15, 20, desired_freezer_temperature)    
    hamburg = rc.ClimateData(average_temperature_hamburg)
    
    heating_demand = hamburg.calculate_yearly_heating_demand(coldRoom)
    for month, demand in zip(hamburg.months, heating_demand):
        print(f"Heating demand in {month}: {demand:.2f} kW")
    rc.Plotter.plot_heating_demand(hamburg.months, heating_demand, average_temperature_hamburg)