# HoundSploit Bash

HoundSploit Bash is an advanced command-line search engine for Exploit-DB developed in Python, born with the
aim of showing the user the most accurate search results.

## Features

* Effective version number filtering
* Open the source code of exploits and shellcodes using _nano_
* View information about the characteristics of exploits and shellcodes
* Automatic check for updates

### Effective version number filtering examples
#### Example I

```
nicolas@carolo:~$ searchsploit WordPress 2.0.2
WordPress 2.0.2- 'cache' Remote Shell Injection
WordPress Plugin Crawl Rate Tracker 2.0.2 - SQL Inject
WordPress Plugin Sodahead Polls 2.0.2 - Multiple Cross
```

```
nicolas@carolo:~$ python houndsploit.py "wordpress 2.0.2"
10 exploits and 0 shellcodes found.

EXPLOITS:
+-------+---------------------------------------------------------------------------------------+
|    ID | DESCRIPTION                                                                           |
+=======+=======================================================================================+
|     6 | WordPress 2.0.2 - 'cache' Remote Shell Injection                                      |
+-------+---------------------------------------------------------------------------------------+
|  4397 | WordPress 1.5.1.1 < 2.2.2 - Multiple Vulnerabilities                                  |
+-------+---------------------------------------------------------------------------------------+
| 10088 | WordPress 2.0 < 2.7.1 - 'admin.php' Module Configuration Security Bypass              |
+-------+---------------------------------------------------------------------------------------+
| 10089 | WordPress < 2.8.5 - Unrestricted Arbitrary File Upload / Arbitrary PHP Code Execution |
+-------+---------------------------------------------------------------------------------------+
| 17755 | WordPress Plugin Crawl Rate Tracker 2.0.2 - SQL Injection                             |
+-------+---------------------------------------------------------------------------------------+
| 29754 | WordPress < 2.1.2 - 'PHP_Self' Cross-Site Scripting                                   |
+-------+---------------------------------------------------------------------------------------+
| 35414 | WordPress < 4.0.1 - Denial of Service                                                 |
+-------+---------------------------------------------------------------------------------------+
| 35475 | WordPress Plugin Sodahead Polls 2.0.2 - Multiple Cross-Site Scripting Vulnerabilities |
+-------+---------------------------------------------------------------------------------------+
| 41497 | WordPress < 4.7.1 - Username Enumeration                                              |
+-------+---------------------------------------------------------------------------------------+
| 41963 | WordPress < 4.7.4 - Unauthorized Password Reset                                       |
+-------+---------------------------------------------------------------------------------------+
```


#### Example II

```
nicolas@carolo:~$ searchsploit Linux Kernel 4.2.3
Exploits: No Result
Shellcodes: No Result
Papers: No Result
```

```
nicolas@carolo:~$ python houndsploit.py "linux kernel 4.2.3"
14 exploits and 0 shellcodes found.

EXPLOITS:
+-------+-------------------------------------------------------------------------------------------------------+
|    ID | DESCRIPTION                                                                                           |
+=======+=======================================================================================================+
| 41995 | Linux Kernel 3.11 < 4.8 0 - 'SO_SNDBUFFORCE' / 'SO_RCVBUFFORCE' Local Privilege Escalation            |
+-------+-------------------------------------------------------------------------------------------------------+
| 42136 | Linux Kernel < 4.10.13 - 'keyctl_set_reqkey_keyring' Local Denial of Service                          |
+-------+-------------------------------------------------------------------------------------------------------+
| 42762 | Linux Kernel < 4.13.1 - BlueTooth Buffer Overflow (PoC)                                               |
+-------+-------------------------------------------------------------------------------------------------------+
| 42932 | Linux Kernel < 4.14.rc3 - Local Denial of Service                                                     |
+-------+-------------------------------------------------------------------------------------------------------+
| 43345 | Linux kernel < 4.10.15 - Race Condition Privilege Escalation                                          |
+-------+-------------------------------------------------------------------------------------------------------+
| 43418 | Linux Kernel < 4.4.0-83 / < 4.8.0-58 (Ubuntu 14.04/16.04) - Local Privilege Escalation (KASLR / SMEP) |
+-------+-------------------------------------------------------------------------------------------------------+
| 44298 | Linux Kernel < 4.4.0-116 (Ubuntu 16.04.4) - Local Privilege Escalation                                |
+-------+-------------------------------------------------------------------------------------------------------+
| 44300 | Linux Kernel < 4.4.0-21 (Ubuntu 16.04 x64) - 'netfilter target_offset' Local Privilege Escalation     |
+-------+-------------------------------------------------------------------------------------------------------+
| 44301 | Linux Kernel < 4.5.1 - Off-By-One (PoC)                                                               |
+-------+-------------------------------------------------------------------------------------------------------+
| 44325 | Linux Kernel < 4.15.4 - 'show_floppy' KASLR Address Leak                                              |
+-------+-------------------------------------------------------------------------------------------------------+
| 44579 | Linux Kernel < 4.17-rc1 - 'AF_LLC' Double Free                                                        |
+-------+-------------------------------------------------------------------------------------------------------+
| 44832 | Linux Kernel < 4.16.11 - 'ext4_read_inline_data()' Memory Corruption                                  |
+-------+-------------------------------------------------------------------------------------------------------+
| 45010 | Linux Kernel < 4.13.9 (Ubuntu 16.04 / Fedora 27) - Local Privilege Escalation                         |
+-------+-------------------------------------------------------------------------------------------------------+
| 45553 | Linux Kernel < 4.11.8 - 'mq_notify: double sock_put()' Local Privilege Escalation                     |
+-------+-------------------------------------------------------------------------------------------------------+
```

## Guide

| ACTION                                     | COMMAND LINE                               |
|--------------------------------------------|--------------------------------------------|
| Perform a search                           | python houndsploit.py "[search text]"      |
| Show info about the exploit                | python houndsploit.py -ie [exploit's id]   |
| Show info about the shellcode              | python houndsploit.py -is [shellcode's id] |
| Open the exploit's source code with nano   | python houndsploit.py -oe [exploit's id]   |
| Open the shellcode's source code with nano | python houndsploit.py -os [shellcode's id] |
| Show software information                  | python houndsploit.py -v                   |
| Show help                                  | python houndsploit.py -help                |
| Check for software updates                 | python houndsploit.py -u                   |
| Check for database updates                 | python houndsploit.py -udb                 |

## Installation procedure

1. Clone or [download the repository](https://github.com/nicolas-carolo/HoundSploitBash/archive/master.zip) of HoundSploit Bash:
    * `$ git clone https://github.com/nicolas-carolo/HoundSploitBash.git`
2. Install [the **interpreter** and the **required tools**](https://github.com/nicolas-carolo/HoundSploitBash/blob/master/documentation/minimum_requirements.md)
3. Create and configure the virtual environment `venv` (optional, but recommended):
    * `$ python -m venv ./venv`
4. Run: `$ python setup.py`
5. Run: `$ python houndsploit.py`

## Documentation

[Here](https://github.com/nicolas-carolo/HoundSploitBash/tree/master/documentation)
you can read the software documentation.

## Updates

Check for software updates:
`$ python houndsploit.py -u`

Check for database updates:
`$ python houndsploit.py -udb`
