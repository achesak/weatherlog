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
    
    if CloudCoverage.SUNNY_MIN <= perc <= CloudCoverage.SUNNY_MAX:
        return CloudCoverageType.SUNNY
    
    elif CloudCoverage.MOSTLY_SUNNY_MIN < perc <= CloudCoverage.MOSTLY_SUNNY_MAX:
        return CloudCoverageType.MOSTLY_SUNNY
    
    elif CloudCoverage.PARTLY_CLOUDY_MIN < perc <= CloudCoverage.PARTLY_CLOUDY_MAX:
        return CloudCoverageType.PARTLY_CLOUDY
    
    elif CloudCoverage.MOSTLY_CLOUDY_MIN < perc <= CloudCoverage.MOSTLY_CLOUDY_MAX:
        return CloudCoverageType.MOSTLY_CLOUDY
    
    elif CloudCoverage.CLOUDY_MIN < perc <= CloudCoverage.CLOUDY_MAX:
        return CloudCoverageType.CLOUDY
