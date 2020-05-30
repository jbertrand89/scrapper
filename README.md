# Google Image Scrapper

## Implementation

### Virtual environment
All the code has been written using Python 3.6.9. You can install the packages from the scrapper_requirements.txt file.

### Using a WebDriver

#### With Chrome

Steps:
* Identify your Chrome version. Typically found by clicking About Google Chrome. I currently have version 83.0.4103.61 (my main version is thus 83, the number before the first dot).
* Download the corresponding ChromeDriver from here for your main version and put the executable into an accessible location. Mine is in the folder <current_folder>/webdriver. 
* Specify the location of your executable in CHROME_DRIVER_PATH (main.py line 8).

#### With Firefox

Steps:
* Download the corresponding GeckoDriver from here and put the executable into an accessible location. Mine is in the folder <current_folder>/webdriver. 
* Specify the location of your executable in FIREFOX_DRIVER_PATH (main.py line 9).

### Main code

Run the code with the default settings.
'''
python main.py
'''

The defaults settings are:
* the query is “dogs”
* the number of images fetched is 10.
* the root data folder will be “data”
* the web browser used is firefox

You can change each default parameter.

For more information, run
'''
python main.py --help
'''
