# AeroSummand
Worker shift statistics and career records for shifts published on the AeroNet web suite.

## Getting Started

### Prerequisites
In order to use AeroSummand, you need to download Chromedriver and the required Python modules. You can download [Chromedriver here](https://chromedriver.chromium.org/downloads). And install the required modules by running: 

```
pip3 install selenium
pip3 install bs4
```

### Usage
AeroNet users with elevated privelleges should use the AeroSummandSUP.py file, and AeroSummand.py otherwise. In either file, the path to the Chromedriver should be specified under WD_PATH.

##### AeroSummand.py
AeroSummand.py is intended for usage by users with default AeroNet access. (i.e. unable to view the rosters of other employees). In the AeroSummand.py file, enter your login credentials in the USERNAME and PASSWORD fields. To get total career statistics, specify both the start date of your contract (i.e. your first day with the company) and the date of the nearest Monday to todays current date. (Both START_DATE and END_DATE should fall on Mondays and be in a YYYY-MM-DD).


##### AeroSummandSUP.py
AeroSummandSUP.py is intended for usage by users with elevated AeroNet access. In the AeroSummandSUP.py file, enter your login credentials in the USERNAME and PASSWORD fields. To get total career statistics of any employee, specify both the start date of their contract (i.e. their first day with the company) and the date of the nearest Monday to todays current date. Enter the desired employee's ID and NAME under EMP_IDENT and EMP_NAME respectively.