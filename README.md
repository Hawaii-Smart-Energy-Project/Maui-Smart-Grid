# Maui Smart Grid Project #

[Daniel Zhang (張道博)](http://www.github.com/dz1111), Software Engineer

## Overview ##

The University of Hawaii at Manoa was tasked with maintaining a data science repository for use by analysts of the [Maui Smart Grid](http://www.mauismartgrid.com) energy sustainability project through the [Hawaii Natural Energy Institute](http://www.hnei.hawaii.edu). This software provides the data acquisition, processing and operational resources necessary to accomplish this task. Source data is acquired in multiple formats including XML, tab-separated values, and comma-separated values. Data storage is dependent on a PostgreSQL database server on the back end. Issues for this project are tracked at the [Hawaii Smart Energy Project YouTRACK instance](http://smart-energy-project.myjetbrains.com/youtrack/rest/agile/).

### Software Features ###

* Open-source (BSD license) code in Python 2.7x and Perl 5.x.
* Parsing of source data is provided for multiple formats.
* Insertion of data to a data store (PostgreSQL 9.1) is performed automatically.
* Source files to recreate the structure of the data store are available.
* Unit testing of data processing operations is provided by a test suite implemented through Python's `unittest`.
* Results of data operations are reported using **email notifications including plots as graphic summaries**.
* Automatic export of live databases to cloud storage for multiple days saved independently.

### Project Documentation ###

This README file is the primary documentation for this software project. Further documentation is also maintained as docstrings within the source code files with the intention of conforming to the reStructuredText format. There is also a [GitHub-based wiki](https://github.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/wiki).

## Implementation ##

The Python code is written in Python 2.7x. It has a testing suite implemented through `unittest`. Python 3 will not be supported until there is a demonstrated need and all dependencies are reviewed.

The database schema is illustrated in `docs/meco-direct-derived-schema-v3.pdf`.

Data parsing is performed by the ElementTree XML parser. Data store operations are implemented through the psycopg2 PostgreSQL library.

Data processing involves inserting nested sets of data linked by their primary keys, generated as sequential integer values, of the preceding table. Foreign keys are determined by a separate class that holds the last primary key used for each table. The design for this feature is illustrated in `docs/fk-value-determiner.pdf`.

### Database Schema ###

A SQL dump, produced by `pg_dump`, of the database schema is provided for reference only.

The schema consists of the following components.

1. MECO Energy Data
2. MECO Event Data
3. MECO Location Records (deprecated)
4. MECO Meter Records (deprecated)
5. MECO Meter Location History
9. MECO eGauge Energy Data
6. NOAA Weather Data (Kahului Airport Station)
7. Circuit Data
8. Transformer Data
10. Irradiance Data
11. PV Service Points
12. Power Meter Events

A [helpful schema diagram](https://github.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/raw/master/diagrams/meco-direct-derived-schema-v3.pdf) is provided in the repository and a version is displayed here illustrating the portion of the schema derived from MECO export data by [SSN (Silver Spring Networks)](http://www.mauismartgrid.com/maui-smart-grid-project-description/project-team/).

![MECO Derived Schema](https://raw.github.com/Hawaii-Smart-Energy-Project/maui-smart-grid/master/diagrams/meco-direct-derived-schema-v3.png)

#### Database Version History ####

v1
: Initial data insertion from first exports. This version is deprecated.

v2
: Eliminated duplicates in the Reading branch by filtering on meter name, interval end time, and channel.

v3 (Production)
: Retroactively adding event data. Duplicate records exist in the Event branch and the Register branch.

v4 (Development)
: Will address duplicates in the Event branch and the Register branch. To include updated weather data.

![MECO Derived Schema](https://raw.github.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/diagrams/2013-07-29_ReadingAndMeterCounts.png)
Plot of readings per meter counts and meter counts per day loaded to meco_v3.

## Installation and Updating ##

A custom automatic installation script, `install-msg.py`, has been developed to provide a single command capable of:

* Creation of a distribution archive from the source code base.
* Installation, or updating of an existing installation, from the installer within the distribution archive.
* Installation of non-Python code such as the MSG eGauge Service.

It is intended to facilitate the maintenace of the software installation, **and** updating, while at the same time allowing development of the source code base. It is used like so

	python install-msg.py --sourcePath ${SOURCE_CODE_BASE_PATH} --installUserPath ${DESTINATION_BASE_PATH}

If the tilde symbol (~) is used as the destination base path, then the software will be installed into a directory titled after the package name and version in the user's home directory. 

The software distribution archive is managed by `distutils` and is in tar gz format. It can be extracted using

    $ tar -zxvf Maui-Smart-Grid-1.0.0.tar.gz

### Software Dependencies ###

The software has the following dependencies and they can be satisfied through various methods. During development, `pip` was used to install third-party modules. Other options exist for installing the necessary dependencies.

#### Python Modules Not in the Standard Library ####

* dateutil
* google-api-python-client
* matplotlib
* psycopg2
* pycurl
* pylab

### Python-Based Scripts and Modules ###

> __WARNING: The Python-based installer is not yet fully working.__

The Python-based scripts and modules have their installer implemented through `distutils`. They can be installed using

	$ cd dist/MauiSmartGrid-1.0.0
	$ python setup.py install --home=~/Maui-Smart-Grid-1.0.0

This example demonstrates installing to a user directory (user-based install) which is sometimes preferred over installing to a system-wide path. This is also referred to as installing using the "home scheme" in the Python documentation. For this example, the `PYTHONPATH` environment variable should be set using something like

	$ export PYTHONPATH=~/Maui-Smart-Grid-1.0.0/lib/python

where this example is specific to bash or sh. This can be placed in a startup configuration file such as `.bashrc`, `.bash_profile` or crontab, as necessary.

### MSG eGauge Service ###

The MSG eGauge Service is installed separately from the rest of the system and uses its own installer in `/src/msg-egauge-service`.

Here's an example installation command.

	$ sudo perl {$PATH_TO_INSTALLER}/installEgaugeAutomaticDataServices.pl

The install script, `/src/msg_egauge_service/installEgaugeAutomaticDataServices.pl`, should be edited to set the install paths as the installer is not as sophisticated as the Python installer. The installer will work if invoked from other paths and does not have to be run from the path containing the source files.

## Distribution ##

The distribution archive is created using

	cd ${MAUI_SMART_GRID_SOURCE_CODE_ROOT_PATH}
	$ python setup.py sdist

### Maintaining the Distribution ###

The files `setup.py` and `MANIFEST.in` require continual updates so that the installer Will be able to install the latest distribution. Specifically, `setup.py` contains all of the files are installed in the `bin` and `lib` paths, while the `MANIFEST.in` contains additional files that are relevant to the distribution.

## Uninstallation ##

It is safe to complete remove the directory to which the software was installed for the purpose of replacing the software while preserving an existing configuration. The configuration settings are not stored in the software installation path and must be removed separately if complete removal is desired.

## Configuration ##

All of the site-specific options are intended to be held in text-based configuration files. 

The software is configured through a text configuration file contained in the user's home directory. The file is named `~/.msg-data-operations.cfg`. Permissions should be limited to owner read/write only. It is read by the `ConfigParser` module. 

In summary, the configuration files are:

* `~/.msg-data-operations.cfg`
* `/usr/local/msg-egauge-service/config/egauge-automatic-data-services.config`

The contents of these files are detailed in the following sections.

### Example Main Configuration File Content ###

The reference template can be found in `config/sample-dot-msg-data-operations.cfg.`

    [Debugging]
    debug=False
    limit_commits=False
    
    [Data Paths]
    # Plot path is where plots will be saved.
    plot_path=${PLOT_PATH}
    
    [MECO Autoload]
    # These are paths related to MECO data autoloading.
    meco_new_data_path=${AUTOLOAD_DATA_PATH}
    Example: /usr/local/smb-share/MECO-DATA-AUTOLOAD

    meco_autoload_archive_path=${AUTOLOAD_ARCHIVE_PATH}
    ## Example: /usr/local/smb-share/.MECO-AUTOLOAD-ARCHIVE

    meco_autoload_failures_path=${AUTOLOAD_FAILURE_PATH}
    ## Example: /usr/local/smb-share/.MECO-AUTOLOAD-FAILURES

    data_load_command=${COMMAND_USED_FOR_INSERTING_MECO_DATA}
    ## Example: python ~/Maui-Smart-Grid-1.0.0/bin/insertMECOEnergyData.py --email > insert.log

    [Executable Paths]
    bin_path=${MECO_BIN_DIR}
	  ## Example: ~/Maui-Smart-Grid-1.0.0/bin
    
    [Notifications]
    email_fromaddr=${EMAIL_ADDRESS}
    email_username=${EMAIL_USERNAME}
    email_password=${EMAIL_PASSWORD}
    email_recipients=${COMMA_SEPARATED_EMAIL_RECIPIENTS}
    testing_email_recipients=${COMMA_SEPARATED_EMAIL_RECIPIENTS}
    email_smtp_server=${SMTP_SERVER_AND_PORT}
    
    [Weather Data]
    
    ## Example URL: http://cdo.ncdc.noaa.gov/qclcd_ascii/
    weather_data_url=${WEATHER_DATA_URL}
    
    ## Example pattern: <A HREF=".*?">(QCLCD(201208|201209|201210|201211|201212|2013).*?)</A>
    weather_data_pattern=${WEATHER_DATA_PATTERN}
    
    weather_data_path=${WEATHER_DATA_PATH}
    
    [Export]
    db_export_path=/home/daniel/msg-db-dumps
    dbs_to_export=${DATABASE_NAME}
    ## Example: meco_v3

    google_api_client_id=${GOOGLE_CLIENT_ID}
    google_api_client_secret=${GOOGLE_CLIENT_SECRET}
    google_api_credentials_path=${GOOGLE_CLIENT_CREDENTIALS_PATH}
    days_to_keep=${NUMBER_OF_DAYS_OF_EXPORTS_TO_KEEP}
    read_permission=${EMAIL_ADDRESSES_TO_GRANT_READER_PERMISSION}

    [Database]
    db_password=${PASSWORD}
    db_host=${IP_ADDRESS_OR_HOSTNAME}
    db_port=${DB_PORT}
    db_username=${DB_USERNAME}

    ## The name of the database that will be used by automated operations.
    db_name=${DB_NAME}
    
    ## The name of the databased used for testing operations.
    testing_db_name=${TESTING_DB_NAME}
    
    [Hardware]
    multiprocessing_limit = ${MULTIPROCESSING_LIMIT}

    [Testing]
    tester_email=${EMAIL_ADDRESS}

### MSG eGauge Service Configuration ###

The following is an example of the configuration file used for configuring the MSG eGauge Service. This file is installed at `/usr/local/msg-egauge-service/config/egauge-automatic-data-services.config`.

    msg_dbname = "${DATABASE_NAME}"
    data_dir = "${DATA_DOWNLOAD_PATH}"
    insert_table = "\"${TABLE_NAME}\""
    loaded_data_dir = "${DATA_ALREADY_LOADED_PATH}"
    invalid_data_dir = "${DATA_PATH_FOR_INVALID_DATA_STORAGE}"
    db_pass = "${DB_PASSWORD}"
    db_user = "${DB_USERNAME}"
    db_host = "${DB_HOST}"
    db_port = "${DB_PORT}"
    
    egauge_user = "${EGAUGE_USERNAME}"
    egauge_password = "${EGAUGE_PASSWORD}"
    
    egauge = ${EGAUGE_ID_1}
    egauge = ${EGAUGE_ID_2}
    egauge = ${EGAUGE_ID_3}

### Database Configuration ###

The database schema can be installed using the following command form where `${DATABASE_NAME}` is a valid database.

    $ psql ${DATABASE_NAME} < ${DATABASE_STRUCTURE}.sql

### Crontab Setup ###

This software system makes use of `cron` for automatic operation scheduling. It is capable of running under a properly configured user-based crontab where the software distribution is installed in a user's home folder.

#### Example User-Based Crontab ####

The following represents an example crontab configuration that can be installed using `crontab -e` with the appropriate substitutions.

	MAILTO=${EMAIL_ADDRESS}
	PYTHONPATH=/home/${USERNAME}/Maui-Smart-Grid-1.0.0/lib/python
	20 * * * * /usr/local/egauge-automatic-data-services/bin/runWithEnvGetEgaugeData.sh
	12 * * * * /usr/local/msg-egauge-service/bin/runWithEnvGetEgaugeData.sh
	40 14 * * 1 /usr/local/bin/msg_egauge_new_data_checker.py
	30 14 * * 2 /usr/local/bin/retrieveNOAAWeatherData.py
	30 15 * * 2 /usr/local/bin/insertCompressedNOAAWeatherData.py --email
	01 03 * * * python ~/Maui-Smart-Grid-1.0.0/bin/exportDBsToCloud.py
	*/15 * * * * python ~/Maui-Smart-Grid-1.0.0/bin/autoloadNewMECOData.py

## Software Operation ##

### Inserting MECO Energy Data from Source XML ###

The exported XML data files contain the energy data. Insertion to the database is performed by running

    $ time python -u ${PATH_TO_SCRIPT}/insertMECOEnergyData.py --email > insert-log.txt
    
in the directory where the data files are contained. The use of `time` is for informational purposes only and is not necessary. Redirecting to `insert-log.txt` is also unneeded but reduces the output to the short form.

#### Sample Output of Data Insertion ####

MECO data is inserted using

    $ insertMECOEnergyData.py --email > insert-run.log 

The output looks like the following and is the concise log output for data loading.
    
    Inserting data to database meco_v3.
    
    3:{0rd,0re,0ev}(0)[3440]<2688rd,56re,0ev,3440,3440>*3:{0rd,0re,0ev}(1)[6880]<2688rd,56re,0ev,
    3440,6880>*3:{0rd,0re,0ev}(2)[10320]<2688rd,56re,0ev,3440,10320>*3:{0rd,0re,0ev}(3)[13760]<2688rd,
    56re,0ev,3440,13760>*3:{0rd,0re,0ev}(4)[20651]<5376rd,112re,10ev,6891,20651>*3:{0rd,0re,0ev}(5)
    [24091]<2688rd,56re,0ev,3440,24091>*3:{0rd,0re,0ev}(6)[27531]<2688rd,56re,0ev,3440,27531>*3:{0rd,0re,
    0ev}(7)[30971]<2688rd,56re,0ev,3440,30971>*3:{0rd,0re,0ev}(8)[37854]<5376rd,112re,2ev,6883,37854>*3:{0rd,
    0re,0ev}(9)[41294]<2688rd,56re,0ev,3440,41294>*3:{0rd,0re,0ev}(10)[44734]<2688rd,56re,0ev,3440,44734>*
    ...
    ---3:{0rd,0re,0ev}(44)[166400]<129024rd,2891re,1019ev,NA,166400>*

Individual processes are denoted by a number and a colon. The numbers in brackets correspond to {dropped duplicates in the reading branch, register branch or the event branch)}, (reading group index), and [element count]. The duplicate count is discrete by group. The element count is cumulative over the data set. 

Dropped reading duplicates are the duplicate entries---determined by meter name, interval end time, and channel number---that are present in the source data. The reading group index is an integer count of the distinct groups of energy readings (MeterData record sets) in the source data. The element count refers to the individual elements within the source data.

Angled brackets contain counts of actual records inserted for each of the branches. They also contain group counts as well as a cumulative count.

The stars (*) indicate when commits are performed.

A final summary report follows the `---` symbol.

Parallel data loading is supported since loading is performed atomically, database commits are made after data verification including taking duplicate records into account. The default data loading mode is parallel loading of multiple files. Duplicate files can be problematic because of this and should, therefore, be eliminated prior to passing data to the autoload.


  
### Testing Mode
The database insertion scripts have a separate testing mode that can be activated using the `--testing` command-line option. When testing mode is enabled, database operations will be performed on the testing database as defined in the site configuration file. Additionally, operations such as notifications will be directed to their appropriate testing mode settings. For example, email notifications will be delivered to testing mode recipients instead of the primary distribution list.

### Inserting Location and Meter Records (DEPRECATED) ###

Location and meter records are stored in separate tab-separated files and are inserted using separate scripts.

    $ insertLocationRecords.py ${FILENAME}

    $ insertMeterRecords.py ${FILENAME}
    
These scripts and their associated data are deprecated in favor of the Meter Location History (MLH).

### Inserting NOAA Weather Data (Kahului Airport Station WBAN 22516) ###

Weather data loading is a two-stage process involving retrieval and insertion.

Retrieval is performed using

    $ retrieveNOAAWeatherData.py
     
Insertion is performed using

    $ insertCompressedNOAAWeatherData.py --email
    
and supports recursive data processing of a set of files from the current directory. Weather data loading supports notifications.

### MSG eGauge Service Operation ###

Initial loading of eGauge energy data can take a longer time than follow-up data loading. It is also more prone to error conditions as it is processing a much larger data set.

Data exists in three possible states:

1. Data that has been downloaded but not yet loaded.
2. Valid data that has been loaded.
3. Invalid data that cannot be loaded.

There are three corresponding directories that are used to maintain the files for the data in these different states. The paths for these directories are defined in the MSG eGauge Service Configuration.

#### Permissions ####

The eGauge data download directory should be group writable if running the MSG eGauge Service from a user account.

#### Invalid Data ####

When invalid data exists, all other data is not loaded. This is a limitation of the eGauge service in its present form. Manual intervention is required to resolve this problem. This condition can be caused when there exists a mismatched number of data values to the data columns. Database operations will not be able to complete when the data is in this state. Data that is not able to be loaded is archived to the invalid data path. It is recommended that this storage be occassionally purged as **invalid data only pertains to the time period between that which was last loaded and the most recent data available.** It is not automatically deleted in case it is needed for reference.

### Database Exports ###

Exports of MSG databases and other databases occur according to a predefined schedule. The exports consist of gzip compressed SQL scripts that are stored both on local storage and cloud storage. Storage to the Google Drive service is supported at this time. Database exports are verified by their MD5 checksums. Individual export archives are shared to a predefined recipient list at the time of export.

### Utility Scripts ###

These scripts are site-dependent.

`grantAllPermissionsToDatabase.sh ${DATABASE}`
: Set appropriate group permissions to databases.

## Notifications ##

Notification of the results of data processing events is provided by the **MSG Notification System**. Notifications are distributed by email to a predefined recipient list (comma-separated) contained in the configuration file.

### MECO Energy Data Loading ###

#### Example Notification for Data Loading ####

    Recursively inserting data to the database named meco_v3.
    Starting in /msg-data/2013_07_10
    insertScript = insertMECOEnergyData.py
    
    ./20130710-99bb8b2b-12a1-4db5-8a1c-7312277cf404-1-1.xml.gz
    
    Inserting data to database meco_v3.
    
    Parsing XML in ./20130710-99bb8b2b-12a1-4db5-8a1c-7312277cf404-1-1.xml.gz.
    {0rd,0re,0ev}(0)[8869]<6912rd,144re,24ev,8869,8869>*{0rd,0re,0ev}(1)[13291]<3456rd,72re,0ev,4422,13291>*{0rd,0re,0ev}(2)[17713]<3456rd,72re,0ev,4422,17713>*{0rd,0re,0ev}(3)[26566]<6912rd,144re,8ev,8853,26566>*{0rd,0re,0ev}  ...  ---{0rd,0re,0ev}(37)[191467]<0rd,0re,0ev,0,191459>*
    
    Wall time = 512.54 seconds.
    
    Log Legend: {} = dupes, () = element group, [] = process for insert elements, <> = <reading insert count, register insert count, event insert count, group insert count,total insert count>, * = commit
    rd = reading, re = register, ev = event
    
    Processed file count is 1.
    
    Plot is attached.
    
The final group, after the `---`, is a summary report of the operations performed.

## License ##

Copyright (c) 2013, University of Hawaii Smart Energy Project  
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of the University of Hawaii at Manoa nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.