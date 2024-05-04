# ddr_analysis_tools

This project contains multiple analysis tools. Some of these tools may be derrived from some other libraries but are adjusted to use in other conditions.

## ddr_POD

This code contains two major class which could perfor POD. 1- POD using singular value decomposition and 2- snapshot POD method. I have varified in certain cases that these two methods results in almost similar eigenmodes, however use these method judiciously. The data to these classes should be provided in 2D matrix form where the time axis lies in first dimention.

## ddr_SPOD

The SPOD class in this module is derrived from pyspod library available online.

## ddr_PSD_welch

This is the class made to use welch's method in performing FFT. The welch's method is already availalbe in scipy. The class in this library uses that.

## ddr_FFT

numpy FFT method is used to perform FFt on the data. The class contains several other methods which could be usefull in plotting and filtering.


---
---
