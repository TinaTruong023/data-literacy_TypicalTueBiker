# Source Folder

This folder contains necessary code like the dataloaders for the different datasets.
Also helpful scripts that were developed during the course of this project are included.

## Script descriptions
 - [BikeDataPlotter.py](BikeDataPlotter.py) Since plots have to be repeated for multiple years, this script is used to quickly create most of the explorative plots for the bike data used in the analysis notebooks. Also plot stylings are defined here.
 - [BikeSeasonalDecomposition.py](BikeSeasonalDecomposition.py) a wrapper for the seasonal decomposition designed to easily handle the data in eco counter format.
 - [Colortheme.py](Colortheme.py) all of the different color pallets used in the plots are defined here.
 - [EventsDataPlotter.py](EventsDataPlotter.py) Helps to quickly mark special dates in cyclists plots.
## Data loader
These modules are responsible for loading and handling the respective datasets. Each dataloader provides several functions to filter the data.
 - [LoadEcoCounterData.py](LoadEcoCounterData.py)
 - [LoadEventsData.py](LoadEventsData.py)
 - [LoadFuelData.py](LoadFuelData.py)
 - [LoadWeatherData.py](LoadWeatherData.py)
