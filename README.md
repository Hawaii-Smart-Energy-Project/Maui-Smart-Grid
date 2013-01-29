# Maui Smart Grid Project

Daniel Zhang

## Overview

Provides data operations for the Maui Smart Grid energy sustainability project.

* Parsing of XML source data.
* Insertion of data to a data store (PostgreSQL 9.1).

## Implementation

Code is written using Python 2.7. It has a testing suite implemented through `unittest`.

The database schema is illustrated in `docs/meco-direct-derived-schema.pdf`.

Data parsing is performed by the ElementTree XML parser. Data store operations are implemented through the `psycopg2` PostgreSQL library.

Data processing involves inserting nested sets of data linked by the primary keys, generated as sequential integer values, of the preceding table. Foreign keys are determined by a separate class that holds the last primary key used for each table. The design for this feature is illustrated in `docs/fk-value-determiner.pdf`.