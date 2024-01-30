
# Tübingen on Two Wheels: Profile a Typical Cyclist
**Authors** Stephan Amann, Tanja Huber, David Kleindiek, Tina Truong

**Date** 30.01.2024

GitHub repository for the final project of the 'Data Literacy' class during the winter term at the Eberhard-Karls Universität Tübingen.

The project report is available [here](doc/Tuebingen_on_Two_Wheels_-_Profile_a_Typical_Cyclist.pdf)

## Overview
This repository contains the research work conducted to analyze biking trends in Tübingen, Germany.
The primary objective of this study is to develop a detailed profile of the typical cyclist in Tübingen by examining bike counting station data and its correlation with various external factors.

## Objectives
 - Analyze cycling patterns in Tübingen using data from bike counting stations.
 - Investigate the impact of weather conditions, fuel prices, and public events on cycling trends.

## Repository Structure

The repository is organized into several directories:

 - [`src/`](src): Contains Python scripts for data processing and analysis.
 - [`eva/`](eva): Jupyter notebooks detailing the analysis, including counter analysis, trend analysis, and correlation studies.
 - [`dat/`](dat): Data files used in the study, including bike counter data, event data, fuel price data, and weather data.
 - [`doc/`](doc): Documentation and figures supporting the analysis.

### Running the code
1. Clone the repository:
```bash
git clone https://github.com/TinaTruong023/data-literacy_TypicalTueBiker.git
cd data-literacy_TypicalTueBiker
```
2. Set Up a Virtual Environment (Optional but Recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install Required Packages:
```bash
pip install -r requirements.txt
```
4. Run The Notebooks:
```bash
jupyter notebook eva/
```
