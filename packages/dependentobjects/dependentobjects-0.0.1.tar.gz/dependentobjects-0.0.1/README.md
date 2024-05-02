This is a basic sample package. It can be used to retrieve all nested dependent objects in Analysis Services or Power BI datasets.
'report_name' variable: Select any name to save the Excel file with that name.
server': Connect to a PowerBI dataset, Analysis Services, or localhost. 
It's assumed that you hold administrative rights for the PowerBI dataset, Analysis Services, or localhost.

The following is a demonstration of how to use the package:

# Please use the path of ADOMD.Net that exists in your system. This has been tested with the path for ADOMD.NET\\160.

from sys import path
ADOMD_Path = "\\Program Files\\Microsoft.NET\\ADOMD.NET\\160"
path.append(ADOMD_Path)
from dependentobjects import DependentObjects as d
Obj =d.DependentObjects()
Obj.setParams(report_name="filename.csv",server="localhost",database="catalog")