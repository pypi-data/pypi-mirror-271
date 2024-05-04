#Prerequisities:
    Before installing this package, ensure that you have the following packages: pandas (version 2.2.1 or higher) and pyadomd (version 0.1.1 or higher).
    It's assumed that you hold administrative rights for the PowerBI dataset, Analysis Services, or localhost.

#Overview 
    This project deals with extracting information about data models objects and their dependencies. 

#Key Project Parameters Explained:
    
    data_source: It provides two options for specifying the data source: "folder" or "live".
                 folder: If you choose folder as the data source, you need to provide a folder path where the project will look for three specific csv files and you should also provide folder_path parameter along with it.
                 live: you can connect to analysis services or powerbi datasets to get their objects and thier dependencies. If you choose live as the data source, you need to provider server, database parameters along with it.
    
    folder_path: it assumes this path contains the tables.csv, measures.csv and calc_dependency.csv files in it. follow the below instructions to generate the following files in dax studio.
    
                 tables.csv: This file contains information about the tables in the data model. You can generate this file in Dax Studio using the provided DAX DMV function:
                 %SQL
                 Select * from $SYSTEM.TMSCHEMA_TABLES
                 
                 measures.csv: This file contains information about the measures defined in the data model. You can generate this file in Dax Studio using the provided DAX DMV function:
                 %SQL
                 select * from $SYSTEM.TMSCHEMA_MEASURES

                 calc_dependency.csv: This file contains information about the calculation dependencies within the data model. You can generate this file in Dax Studio using the provided DAX DMV function:
                 %SQL
                 select * from $SYSTEM.DISCOVER_CALC_DEPENDENCY

    server: The server name or address of the Analysis Services server, Power BI dataset server, or even your local machine.

    database: The specific catalog name or ID of the data model you want to analyze.

    Additional Parameter:
                 filename: This parameter allows you to specify the desired filename for the output CSV file containing the extracted nested dependent objects. This file is created after you call the set_parameters method within the project.
                 adomd_path: This parameter specifies the location of the ADOMD.NET library, which is required if you're connecting directly using Analysis Services or live Power BI datasets. The project assumes you have Analysis Services installed and points to the default location for the latest version.
                             please utlize the double \\ instead of single \\\\ in ADOMD_Path

    Note: The version number in the adomd_path might change depending on the specific Analysis Services version you have installed.
          If you don't have Analysis Services and choose the database connection method, you'll need to download and install SQL Server from Microsoft's website (https://www.microsoft.com/en-us/sql-server/sql-server-downloads) and ensure Analysis Services is included during the custom installation process.


By providing these parameters, the project can either read the data model information from the specified CSV files or connect directly to the database and extract details about the  measures, calc_column, calc_tables and their dependencies within the data model.


#Follow the below demonstration on how to use the package: 

#if data_source is the folder option then use the below code:
#code:
from dependentobjects import DependentObjects  
DependentObjects.set_parameters(data_source="excel", folder_path = r"C:\Users\v-vare\Downloads\data",filename = "testing")

#if data_source is the live option then use the below code:
from dependentobjects import DependentObjects  
DependentObjects.set_parameters(data_source="folder or live", server = localhost , database = catalogname)