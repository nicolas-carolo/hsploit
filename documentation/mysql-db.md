# How to create a MySQL DB for HoundSploit

## Download and configure MySQL

Download and install MySQL for your platform. I suggest you also to install _MySQLWorkbench_ if you want a GUI for
manage the DB.

## Create HOUNDSPLOIT DB connection and the relative tables

### New Automated procedure

1. Run `python setup.py`
2. If the setup is terminated successfully, now you can run _HoundSploit_. 

### Old Automated procedure

**N.B.:** For the following steps, if your computer is running macOS, you have to run the command `/usr/local/mysql/bin/mysql -u root -p [...]`
instead of the command `mysql -u root -p [...]`.

1. Go to `sql_scripts` directory.
2. Run `houndsploit_db_setup.sql script`: `$ mysql -u root -p < houndsploit_db_setup.sql`
3. Run also the following scripts:
    * `files_exploits.sql`: `$ mysql -u root -p HOUNDSPLOIT < files_exploits.sql`
    * `files_shellcodes.sql`: `$ mysql -u root -p HOUNDSPLOIT < files_shellcodes.sql`
    * `files_exceptions.sql`: `$ mysql -u root -p HOUNDSPLOIT < files_exceptions.sql`
4. Now you can run _HoundSploit_.

### Manual procedure: starting from .csv files
1. Get `files_exploits.csv` and `files_shellcodes.csv` from the
[Exploit-DB repository on GitHub](https://github.com/offensive-security/exploitdb).
2. Now you have to create a SQL script for each file. For example I have used the online converter available on this
site: [http://convertcsv.com/csv-to-sql.htm](http://convertcsv.com/csv-to-sql.htm). Creating the two scripts remember
that the exploits table have to be named as `searcher_exploit`, while the shellcodes table as `searcher_shellcode`.
After making the convertion, download and save the two SQL scripts you have just created. I have saved them respectively
as `files_exploits.sql` and `files_shellcodes.sql`. 

### Manual procedure: starting from SQL scripts

1. Open MySQL: `$ mysql -u root -p`
2. Create a new schema named `HOUNDSPLOIT`: `mysql> CREATE DATABASE IF NOT EXISTS HOUNDSPLOIT CHARACTER SET utf32;`
This choice is necessary because some vulnerabilities' authors have names that contain a set of characters that belong
to a great variety of alphabets.
3. Create `searcher_exploit`, `searcher_shellcode` and `searcher_suggestion` tables running the following scripts:
    * `files_exploits.sql`: `$ mysql -u root -p HOUNDSPLOIT < sql_scripts/files_exploits.sql`
    * `files_shellcodes.sql`: `$ mysql -u root -p HOUNDSPLOIT < sql_scripts/files_shellcodes.sql`
    * `files_exceptions.sql`: `mysql -u root -p HOUNDSPLOIT < sql_scripts/files_exceptions.sql`
4. Create a new db user:

    user: `hound-user`
    
    password: `Hound-password9`
    
    using the following command: `mysql> CREATE USER IF NOT EXISTS 'hound-user'@'localhost' IDENTIFIED BY 'Hound-password9';`

    and assign him the privileges to run `ALTER`, `CREATE`, `DELETE`, `INSERT`, `REFERENCES`, `SELECT`, `UPDATE` operations:
   
    `mysql> GRANT ALTER, CREATE, DELETE, INSERT, REFERENCES, SELECT, UPDATE ON 'HOUNDSPLOIT'.* TO 'hound-user'@'localhost' IDENTIFIED BY 'Hound-password9';`
   
5. Now you can run _HoundSploit_ and test if it works fine!


