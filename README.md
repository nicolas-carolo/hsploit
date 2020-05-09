# hsploit.  An advanced command-line search engine for Exploit-DB

```
.__                   .__         .__  __
|  |__   ____________ |  |   ____ |__|/  |_              __    
|  |  \ /  ___/\____ \|  |  /  _ \|  \   __\ (\,--------'()'--o
|   Y  \___ \ |  |_> >  |_(  <_> )  ||  |    (_    ___    /~" 
|___|  /____  >|   __/|____/\____/|__||__|     (_)_)  (_)_)    
     \/     \/ |__|                         

```

Author: Nicolas Carolo <nicolascarolo.dev@gmail.com>

Copyright: © 2020, Nicolas Carolo.

Date: 2020-05-09

Version: 2.0.2


## PURPOSE

_hsploit_ is an advanced command-line search engine for Exploit-DB developed in Python, born with the
aim of showing the user the most accurate search results.

### Features

* Effective version number filtering
* Advanced filtering
* Fast search
* View search results in a table with keywords highlighting
* View search results in a table without keywords highlighting
* View search results without a table
* Save search results into a text file
* Search suggestions with customization
* Open the source code of exploits and shellcodes using _vim_
* View information about the characteristics of exploits and shellcodes
* Copy an exploit or a shellcode file into a directory specified by the user
* Automatic check for database update and for hsploit updates

![Demo](/media/demo.gif)

#### Effective version number filtering examples

```
nicolas@carolo:~$ hsploit -s "wordpress core 2.0.2"

11 exploits and 0 shellcodes found.

EXPLOITS:

+-------+--------------------------------------------------------------------------------------------+
|    ID | DESCRIPTION                                                                                |
+=======+============================================================================================+
| 35414 | WORDPRESS CORE < 4.0.1 - Denial of Service                                                 |
+-------+--------------------------------------------------------------------------------------------+
| 47800 | WORDPRESS CORE < 5.3.x - 'xmlrpc.php' Denial of Service                                    |
+-------+--------------------------------------------------------------------------------------------+
|     6 | WORDPRESS CORE 2.0.2 - 'cache' Remote Shell Injection                                      |
+-------+--------------------------------------------------------------------------------------------+
|  4397 | WORDPRESS CORE 1.5.1.1 < 2.2.2 - Multiple Vulnerabilities                                  |
+-------+--------------------------------------------------------------------------------------------+
| 10088 | WORDPRESS CORE 2.0 < 2.7.1 - 'admin.php' Module Configuration Security Bypass              |
+-------+--------------------------------------------------------------------------------------------+
| 10089 | WORDPRESS CORE < 2.8.5 - Unrestricted Arbitrary File Upload / Arbitrary PHP Code Execution |
+-------+--------------------------------------------------------------------------------------------+
| 29754 | WORDPRESS CORE < 2.1.2 - 'PHP_Self' Cross-Site Scripting                                   |
+-------+--------------------------------------------------------------------------------------------+
| 41497 | WORDPRESS CORE < 4.7.1 - Username Enumeration                                              |
+-------+--------------------------------------------------------------------------------------------+
| 41963 | WORDPRESS CORE < 4.7.4 - Unauthorized Password Reset                                       |
+-------+--------------------------------------------------------------------------------------------+
| 44949 | WORDPRESS CORE < 4.9.6 - (Authenticated) Arbitrary File Deletion                           |
+-------+--------------------------------------------------------------------------------------------+
| 47690 | WORDPRESS CORE < 5.2.3 - Viewing Unauthenticated/Password/Private Posts                    |
+-------+--------------------------------------------------------------------------------------------+


##### Example II

```
nicolas@carolo:~$ searchsploit Linux Kernel 4.2.3
Exploits: No Result
Shellcodes: No Result
Papers: No Result
```

```
nicolas@carolo:~$ hsploit -s "linux kernel 4.4.1"

14 exploits and 0 shellcodes found.

EXPLOITS:

+-------+--------------------------------------------------------------------------------------------------+
|    ID | DESCRIPTION                                                                                      |
+=======+==================================================================================================+
| 42136 | LINUX KERNEL < 4.10.13 - 'keyctl_set_reqkey_keyring' Local Denial of Service                     |
+-------+--------------------------------------------------------------------------------------------------+
| 42762 | LINUX KERNEL < 4.13.1 - BlueTooth Buffer Overflow (PoC)                                          |
+-------+--------------------------------------------------------------------------------------------------+
| 42932 | LINUX KERNEL < 4.14.rc3 - Local Denial of Service                                                |
+-------+--------------------------------------------------------------------------------------------------+
| 44301 | LINUX KERNEL < 4.5.1 - Off-By-One (PoC)                                                          |
+-------+--------------------------------------------------------------------------------------------------+
| 44579 | LINUX KERNEL < 4.17-rc1 - 'AF_LLC' Double Free                                                   |
+-------+--------------------------------------------------------------------------------------------------+
| 44832 | LINUX KERNEL < 4.16.11 - 'ext4_read_inline_data()' Memory Corruption                             |
+-------+--------------------------------------------------------------------------------------------------+
| 39277 | LINUX KERNEL 4.4.1 - REFCOUNT Overflow Use-After-Free in Keyrings Local Privilege Escalation (1) |
+-------+--------------------------------------------------------------------------------------------------+
| 40003 | LINUX KERNEL 4.4.1 - REFCOUNT Overflow Use-After-Free in Keyrings Local Privilege Escalation (2) |
+-------+--------------------------------------------------------------------------------------------------+
| 39772 | LINUX KERNEL 4.4.x (Ubuntu 16.04) - 'double-fdput()' bpf(BPF_PROG_LOAD) Privilege Escalation     |
+-------+--------------------------------------------------------------------------------------------------+
| 41995 | LINUX KERNEL 3.11 < 4.8 0 - 'SO_SNDBUFFORCE' / 'SO_RCVBUFFORCE' Local Privilege Escalation       |
+-------+--------------------------------------------------------------------------------------------------+
| 43345 | LINUX KERNEL < 4.10.15 - Race Condition Privilege Escalation                                     |
+-------+--------------------------------------------------------------------------------------------------+
| 44325 | LINUX KERNEL < 4.15.4 - 'show_floppy' KASLR Address Leak                                         |
+-------+--------------------------------------------------------------------------------------------------+
| 45010 | LINUX KERNEL < 4.13.9 (Ubuntu 16.04 / Fedora 27) - Local Privilege Escalation                    |
+-------+--------------------------------------------------------------------------------------------------+
| 45553 | LINUX KERNEL < 4.11.8 - 'mq_notify: double sock_put()' Local Privilege Escalation                |
+-------+--------------------------------------------------------------------------------------------------+

#### Advanced filtering

Using the advanced search (`-sad` option) you can use the following filters for filtering search
results:
* Search operator: `AND` or `OR`
* Author
* Type
* Platform
* Port
* Date interval

![Advanced Search](/media/sad.gif)


#### Search suggestions

You can choose to show a particular suggestion for a given searched string.
For each case you can also decide to use automatic replacement or not.
It is possible to add new suggestions and delete the existing suggestions.

##### Example of default suggestion:
![Default search suggestions](/media/default_suggestion.gif)

##### Example of autoreplacement
![Search autoreplacement](/media/autoreplacement.gif)


## MINIMUM REQUIREMENTS

### Supported OS

* Linux
* macOS

### Interpreter and tools

* Python 3
* SQLite 3
* vim
* git

## INSTALLATION

### Linux (not-root user) [recommended]
We can install hsploit simply by doing:
```sh
$ git clone https://github.com/nicolas-carolo/hsploit
$ cd hsploit
$ ./install_db_linux.sh
$ pip install -r requirements.txt
$ python setup.py install
```
Now you can remove the repository of _hsploit_ you have downloaded, because this repository has been cloned in `~/HoundSploit/hsploit` for supporting automatic updates.

### Linux (root user)
We can install hsploit simply by doing:
```sh
$ git clone https://github.com/nicolas-carolo/hsploit
$ cd hsploit
$ mkdir /root/HoundSploit
$ touch /root/HoundSploit/enable_root.cfg
$ ./install_db_linux.sh
$ pip install -r requirements.txt
$ python setup.py install
```
Now you can remove the repository of _hsploit_ you have downloaded, because this repository has been cloned in `~/HoundSploit/hsploit` for supporting automatic updates.

### macOS
We can install hsploit simply by doing:
```sh
$ git clone https://github.com/nicolas-carolo/hsploit
$ cd hsploit
$ ./install_db_darwin.sh
$ pip install -r requirements.txt
$ python setup.py install
```
Now you can remove the repository of _hsploit_ you have downloaded, because this repository has been cloned in `~/HoundSploit/hsploit` for supporting automatic updates.

## USAGE
### Search
* Perform a search:
   ```sh
   $ hsploit -s "[search text]"
   ```
* Perform a search (without keywords highlighting):
   ```sh
   $ hsploit -s --nokeywords "[search text]"
   ```
* Perform a search (no table for results):
   ```sh
   $ hsploit -s --notable "[search text]"
   ```
* Perform a search (saving the output into a file):
   ```sh
   $ hsploit -s --file [filename] "[search text]"
   ```

### Advanced search
* Perform an advanced search:
   ```sh
   $ hsploit -sad "[search text]"
   ```
* Perform an advanced search (without keywords highlighting):
   ```sh
   $ hsploit -sad --nokeywords "[search text]"
   ```
* Perform an advanced search (no table for results):
   ```sh
   $ hsploit -sad --notable "[search text]"
   ```
* Perform an advanced search (saving the output into a file):
   ```sh
   $ hsploit -sad --file [filename] "[search text]"
   ```

### Show information about exploits/shellcodes
* Show info about the exploit:
   ```sh
   $ hsploit -ie [exploit's id]
   ```
* Show info about the shellcode:
   ```sh
   $ hsploit -is [shellcode's id]
   ```
* Open the exploit's source code with vim:
   ```sh
   $ hsploit -oe [exploit's id]
   ```
* Open the shellcode's source code with vim:
   ```sh
   $ hsploit -os [shellcode's id]
   ```

### Exploit/Shellcode file management
* Copy the exploit's file into a chosen file or directory:
   ```sh
   $ hsploit -cpe [exploit's id] [file or directory]
   ```
* Copy the shellcode's file into a chosen file or directory:
   ```sh
   $ hsploit -cps [shellcode's id] [file or directory]
   ```

### Suggestions
* List suggestions:
   ```sh
   $ hsploit -ls
   ```
* Add or edit a suggestion:
   ```sh
   $ hsploit -as [keyword(s)]
   ```
* Remove a suggestion:
   ```sh
   $ hsploit -rs [keyword(s)]
   ```

### _hsploit_: updates, information and guide
* Show software information:
   ```sh
   $ hsploit -v
   ```
* Check for software and database updates:
   ```sh
   $ hsploit -u
   ```
* Show help:
   ```sh
   $ hsploit -help
   ```


## COPYRIGHT

Copyright © 2020, Nicolas Carolo.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions, and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions, and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

3. Neither the name of the author of this software nor the names of
   contributors to this software may be used to endorse or promote
   products derived from this software without specific prior written
   consent.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
