# PE-SVF
A toolbox based on ArcGIS 10.6 for the evaluation of positional error in SVF measurements (PE-SVF)

# Background
The **sky-view factor (SVF)** is one of the most critical indicators to characterize urban physical environments. The SVF in the urban street canyon is a single point-specific measurement that can only represent the ratio of the visible sky of a specific point, rather than the ratio of the entire urban street canyon. The change in the location of the SVF observation point will cause significant variation in the SVF value. The **positional error of the SVF observation point (PE-SVFOP)** to the measurement of the SVF for specific applications is often ignored.  
This project is developed for the evaluation of **positional error in SVF measurements (PE-SVF)** by comparing the SVF estimated at the **desired SVF observation point** and **the corresponding actual SVF observation point**.

# What's new 2020.12.20:
We have added the support for ArcGIS Desktop 10.7 and ArcGIS Desktop 10.8.  

# Sample Input Dataset
(1) **3d_buildings.shp** - 3D vector polygonal data of urban buildings   
(2) **point1.shp** - single SVF observation point   
(3) **DOP.shp** - desired SVF observation point   
(4) **AOP.shp** - actual SVF observation point

# Sample Output Dataset
(1) **SVF.csv** - results of SVF calulated for point1.shp  
(2) **PESVF.csv** - results of PE-SVF for DOP.shp and AOP.shp  
(3) **RPESVF.csv** - results of relative PE-SVF (RPE-SVF) for DOP.shp and AOP.shp     

# Toolbox and Script Folder
(1) **SVF Calculation Toolbox.tbx** - a toolbox based on ArcGIS 10.6 to calculate the SVF, PE-SVF and RPE-SVF values from specific SVF observation points of **actual SVF observation point** and **desired SVF observation point**  
(2) **SVF_Calculation_Script** - Python source codes to calculate SVF, PE-SVF and RPE-SVF in SVF Calculation Toolbox.tbx  

# Helper Folder
(1) **Toolbox Helper.pdf** - a tutorial on using the provided toolbox to calculate SVF, PE-SVF and RPE-SVF

# Usage
For examples, please refer to the [Documentation](https://github.com/encyclopedia1998/PE-SVF/tree/main/Helper)

# License
Distributed under the [MIT License](https://choosealicense.com/licenses/mit/). See LICENSE for more information.

