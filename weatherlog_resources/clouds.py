# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: clouds.py
# This module converts cloudiness percentage to a human readable term.
#
################################################################################


# Import application modules.
from weatherlog_resources.openweathermap.constants import CloudCoverage
from weatherlog_resources.constants import * 


def percent_to_term(perc):
    """Converts cloudiness percentage to a human readable term."""
    
    if perc >= CloudCoverage.SUNNY_MIN and perc <= CloudCoverage.SUNNY_MAX:
        return CloudCoverageType.SUNNY
    
    elif perc > CloudCoverage.MOSTLY_SUNNY_MIN and perc <= CloudCoverage.MOSTLY_SUNNY_MAX:
        return CloudCoverageType.MOSTLY_SUNNY
    
    elif perc > CloudCoverage.PARTLY_CLOUDY_MIN and perc <= CloudCoverage.PARTLY_CLOUDY_MAX:
        return CloudCoverageType.PARTLY_CLOUDY
    
    elif perc > CloudCoverage.MOSTLY_CLOUDY_MIN and perc <= CloudCoverage.MOSTLY_CLOUDY_MAX:
        return CloudCoverageType.MOSTLY_CLOUDY
    
    elif perc > CloudCoverage.CLOUDY_MIN and perc <= CloudCoverage.CLOUDY_MAX:
        return CloudCoverageType.CLOUDY
