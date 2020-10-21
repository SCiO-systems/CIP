# SCiO Spectral Indices Prospects

SCiO Spectral Indices Prospects (SIPs) is a dataset containing historical data and projections for two dimensionless indices relevant to climate and environmental science, but usable in various use cases. The indices are:

1. Normalized Difference Vegetation Index ([NDVI](https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index)): Effects like deforestation, desertification, and land degradation are directly related to climate change and human activities. Lang coverage as well as qualitative characteristics related to plant and crops health, can be monitored and assessed via the usage of satellite imaging and its analysis for the calculation of metrics like the Normalized Difference Vegetation Index (NDVI). NDVI is used to determine land use (arable crops, permanent crops, forests, deserts) by analyzing the light reflectance of an area in different spectra. In combination with other data, it is also used to estimate crop health and yield production for various cultivations.
2. Soil Moisture Index (SMI) [^1]: Soil moisture is one of the essential environmental variables per the United Nations and plays a critical role in agriculture, ecology, and meteorology. It is one of the major factors for determining the success of a harvest and the sustainability of local flora, since most vegetation obtains the water it needs from the soil. Satellite imagery along with Digital Elevation Maps and climatic measurements are used for calculating the Soil Moisture Index (SMI), an indicator for the amount of water present between soil surface and groundwater level, from where it is uptaken by plants.

## Temporal coverage

SIPs operate at a yearly step. Historical coverage starts from 1982 for NDVI and 1979 for SMI, while predictions reach up to 2099 for both indices.

## Spatial coverage

The current version (v1.0) of SIPs includes data for 7 countries and their first-level administrative jurisdictions. Future versions will expand the geographical coverage of the dataset. The geographic coverage of each SIPs version can be monitored via the relevant [report](https://github.com/SCiO-systems/SIP/blob/main/Geographic%20Coverage.md).

## Prediction generation methodology

SIPs predictions are based on the [ARIMA model](https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average) which is widely used for timeseries predictions. More specifically, we used the ARIMAX model, i.e. an ARIMA model with the integration of exogenous variables for prediction calculation. For SIPS, we use maximum average temperature and average precipitation as exogenous variables.

For ARIMAX to operate, we need historical data for the targeted variables and both historical and predictive data (for the targeted prediction timeframe) for the exogenous variables. Historical values for the indices were retrieved from the [NOAA Climate Data Record (CDR)](https://data.nodc.noaa.gov/cgi-bin/iso?id=gov.noaa.ncdc:C00813) and the [ESA CCI Soil Moisture Product](https://www.esa-soilmoisture-cci.org/node/238) datasets for NDVI and SMI respectively. Historical values for the exogenous variables were produced using data from the [WorldClim Monthly Data](https://www.worldclim.org/data/monthlywth.html) collection, a downscale of [CRU-TS-4.0.3](https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_4.03/). Yearly values are calculated by computing the average of monthly values as provided by the original dataset. Finally, predictive values for the exogenous variables were retrieved from the [NASA Earth Exchange (NEX) dataset](https://www.nasa.gov/nex).

## Browsing the dataset

### Dataset structure

The SIPs dataset comprises CSV files organised per geographical area and index. Naming follows the `idx_<area_code>_<index>` convention, where `<area_code>` refers to the specifier of the area and `<index>`, refers to the index covered by the file (NDVI or SMI).

Each file includees three columns: `Year`, `rcp4.5_<index>` and `rcp8.5_<index>`, where `<index>`, as before, refers to the index covered by the file. The `rcp` columns provide the predictions for the respective index based on two global development scenarios expressed as Representative Concentration Pathways ([RCPs](https://sedac.ciesin.columbia.edu/ddc/ar5_scenario_process/RCPs.html)), RCP4.5 and RCP8.5.

### Country and Region specifier encoding

The following table summarises the encoding used for the country specifiers throughout the dataset(the `area_code` parameter in the respective filenames). Detailed specifier codes, including codes uses for each country first administration level (regions) can be found at the Region Codes [file](https://github.com/SCiO-systems/SIP/blob/main/Region%20Codes.md) in the SIPs repository.

#### Country codes

| Code | Country      |
| ---- | ------------ |
| IR   | Iran         |
| KZ   | Kazakhstan   |
| KG   | Kyrgyzstan   |
| MN   | Mongolia     |
| TJ   | Tajikistan   |
| TM   | Turkmenistan |
| UZ   | Uzbekistan   |

[^1 ]: Saha, Arnab & Patil, Manti & Goyal, Vikas & Rathore, Devendra. (2018). Assessment and Impact of Soil Moisture Index in Agricultural Drought Estimation using Remote Sensing and GIS Techniques. 5802. DOI: [10.3390/ECWS-3-05802](http://dx.doi.org/10.3390/ECWS-3-05802)
