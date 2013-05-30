# Maui Smart Grid Project

[Daniel Zhang (張道博)](http://www.github.com/dz1111), Software Developer

## Overview

This software provides data operations for the [Maui Smart Grid](http://www.mauismartgrid.com) energy sustainability project for the [Hawaii Natural Energy Institute](http://www.hnei.hawaii.edu). Source data arrives in multiple formats including XML, tab-separated values, and comma-separated values. Issues for this project are tracked at the [Hawaii Smart Energy Project YouTRACK instance](http://smart-energy-project.myjetbrains.com/youtrack/rest/agile/).

### Software Features
* Open-source (BSD license) code in Python 2.7x.
* Parsing of source data is provided for multiple formats.
* Insertion of data to a data store (PostgreSQL 9.1) is performed by executing a script from the command-line.
* Source files to recreate the structure of the data store are available.
* Unit testing of data processing operations is provided by a test suite implemented through Python's `unittest`.

### Project Documentation
Documentation is maintained as docstrings within the source code files with the intention of conforming to the reStructuredText format. There is also a [GitHub-based wiki](https://github.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/wiki).

## Implementation

The code is written in Python 2.7x. It has a testing suite implemented through `unittest`.

The database schema is illustrated in `docs/meco-direct-derived-schema-v3.pdf`.

Data parsing is performed by the ElementTree XML parser. Data store operations are implemented through the psycopg2 PostgreSQL library.

Data processing involves inserting nested sets of data linked by their primary keys, generated as sequential integer values, of the preceding table. Foreign keys are determined by a separate class that holds the last primary key used for each table. The design for this feature is illustrated in `docs/fk-value-determiner.pdf`.

### Database Schema
A SQL dump, produced by `pg_dump`, of the database schema is provided for reference only.

The schema consists of the following components.

1. Energy data
    * Event data is not included in the schema (Event data is scheduled for inclusion in Version 3)
2. Location Records
3. Meter Records
4. Weather Data (Kahalui Station)

A [helpful schema diagram](https://github.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/raw/master/diagrams/meco-direct-derived-schema-v3.pdf) is provided in the repository and a version is displayed here.

![MECO Derived Schema](https://raw.github.com/Hawaii-Smart-Energy-Project/maui-smart-grid/master/diagrams/meco-direct-derived-schema-v3.png)

#### Database Version History
v1
: Initial data insertion from first exports. This version is deprecated.

v2
: Eliminated duplicates in the Reading branch by searching on meter name, interval end time, and channel.

v3
: Retroactively adding event data. 


![MECO Derived Schema](https://raw.github.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid/master/diagrams/2013-05-29_ReadingAndMeterCounts.png)
Plot of readings per meter counts and meter counts per day loaded to meco_v3.

## Configuration

The software is configured through a text configuration file contained in the user's home directory. The file is named `~/meco-data-operations.cfg`. Permissions should be limited to owner read/write only. It is read by the `ConfigParser` module. 

### Example Configuration File Content

The reference template can be found in `config/sample-dot-meco-data-operations.cfg.`

    [Debugging]
    debug=False
    limit_commits=False
    
    [Data Paths]
    plot_path=${MECO_PLOT_PATH}
    
    [Executable Paths]
    bin_path=${MECO_BIN_DIR}
    
    [Notifications]
    email_fromaddr=${EMAIL_FROM_ADDRESS}
    email_username=${SMTP_USERNAME}
    email_password=${EMAIL_SEND_PASSWORD}
    email_recipients=${LIST_OF_EMAIL_RECIPIENTS}
    testing_email_recipients=${LIST_OF_TESTING_EMAIL_RECIPIENTS}
    email_smtp_server=${SMTP_SERVER_ADDRESS}

    [Database]
    db_password=${PASSWORD}
    db_host=${IP_ADDRESS_OR_HOSTNAME}
    db_name=${DB_NAME}
    db_port=${DB_PORT}
    db_username=${DB_USERNAME}
    testing_db_name=${TESTING_DB_NAME}
    
## Database Configuration

The database schema can be installed using the following command form where `${DATABASE_NAME}` is a valid database.

    $ psql ${DATABASE_NAME} < meco-data-schema.sql

## Software Operation

### Inserting Data from Source XML

The exported XML data files contain the energy data. Insertion to the database is performed by running

    $ time python -u ${PATH_TO_SCRIPT}/insertData.py > insert-log.txt
    
in the directory where the data files are contained. The use of `time` is for informational purposes only and is not necessary. Redirecting to `insert-log.txt` is also unneeded but reduces the output to the short form.

#### Sample Output of Data Insertion

    ~/msg-data/2013_02_25_download$ time python -u ~/dzmbp-maui-smart-grid/src/insertData.py > insert-run.log 
    Inserting data to database meco_v2.
    parsing xml in ./20130225-91a9f952-5ef4-46bb-ac33-5fd9f82c3264-1-1.xml.gz
    {0}[0](6868){0}[1](17380){0}[2](20815){0}[3](24250){0}[4](31286){0}[5](34716){0}[6](38146){dupe on insert-->}{1536}[7](46938){0}[8](50374)
    parsing xml in ./20130225-91a9f952-5ef4-46bb-ac33-5fd9f82c3264-2-1.xml.gz
    {0}[0](57257){0}[1](60692){0}[2](67716){0}[3](71151){0}[4](74586){0}[5](78021){0}[6](88336){0}[7](91766){dupe on insert-->}{3136}[8](112881)
    real    4m16.162s
    user    0m58.716s
    sys     0m30.186s

The numbers in brackets correspond to {dropped duplicates (in the reading branch)}, [reading group index], and (element count). Dropped duplicates are the duplicate entries---determined by meter name, interval end time, and channel number---that are present in the source data. The reading group indexes is an integer count of the distinct groups of energy readings in the source data. The element count refers to the individual elements within the source data.
  
### Inserting Location and Meter Records

Location and meter records are stored in separate tab-separated files and are inserted using separate scripts.

    $ insertLocationRecords.py ${FILENAME}

    $ insertMeterRecords.py ${FILENAME}

### Inserting Weather Data (Kahalui Station)

    $ insertWeatherData.py ${FILENAME}

### Utility Scripts

`grantAllPermissionsToDatabase.sh ${DATABASE}`
: Set appropriate permissions to databases.

## License

Copyright (c) 2013, University of Hawaii Smart Energy Project  
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of the University of Hawaii at Manoa nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
