"""Support for Avio EMaxx system for Selectronic's SP Pro inverters."""
import logging
import re

import voluptuous as vol

from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    CONF_IP_ADDRESS,
    CONF_NAME,
)

DOMAIN = "arvio_emaxx"

_LOGGER = logging.getLogger(__name__)

ICON = "mdi:flash"
CONST_DEFAULT_HOST = "emaxx"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_IP_ADDRESS, default=CONST_DEFAULT_HOST): cv.string,
        vol.Optional(CONF_NAME, default=""): cv.string,
    }
)

UNIQUEID_REGEX = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)(?<!_)[A-Z](?=[a-z]))')

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    add_entities([
        ArvioEmaxxSensor(
            config[CONF_IP_ADDRESS],
            "Selectronic Battery State of Charge",
            "battery_soc_percent", "%", SensorDeviceClass.BATTERY, SensorStateClass.MEASUREMENT),

        ArvioEmaxxSensor(
            config[CONF_IP_ADDRESS],
            "Selectronic Power Used",
            "power_used_watts", "W", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),
        ArvioEmaxxSensor(
            config[CONF_IP_ADDRESS],
            "Selectronic Export Power",
            "export_power_watts", "W", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),
        ArvioEmaxxSensor(
            config[CONF_IP_ADDRESS],
            "Selectronic AC Load Power",
            "ac_load_power_watts", "W", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),

        ArvioEmaxxSensor(
            config[CONF_IP_ADDRESS],
            "Selectronic Exported Power Total",
            "export_kilowatt_hours", "kWh", SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
        ArvioEmaxxSensor(
            config[CONF_IP_ADDRESS],
            "Selectronic AC Load Total",
            "ac_load_kilowatt_hours", "kWh", SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
        ArvioEmaxxSensor(
            config[CONF_IP_ADDRESS],
            "Selectronic AC Input Power Total",
            "ac_input_kilowatt_hours", "kWh", SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
    
        ArvioEmaxxSensor(
            config[CONF_IP_ADDRESS],
            "Selectronic Battery Input Total",
            "battery_input_kilowatt_hours", "kWh", SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
        ArvioEmaxxSensor(
            config[CONF_IP_ADDRESS],
            "Selectronic Battery Output Total",
            "battery_output_kilowatt_hours", "kWh", SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
    ])


class ArvioEmaxxSensor(SensorEntity):
    """Representation of a Sensor."""
    
    def __init__(self, endpoint, name, type, units, device_class, state_class):
        """Initialize the sensor."""
        self._endpoint = endpoint
        self._name = name
        self._type = type
        self._state = None
        self._device_class = device_class
        self._state_class = state_class
        self._units = units
        self._unique_id = UNIQUEID_REGEX.sub(r'_\1', name).lower()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self):
        """Returns the unique ID for this entity"""
        return self._unique_id

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state
    
    @property
    def device_class(self):
        """Return the state of the sensor."""
        return self._device_class

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._units

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def state_class(self):
        """Returns the state class for this entity"""
        return self._state_class

    async def async_update(self):
        """Get the data from the Arvio Emaxx."""
        from arvio_emaxx_reader.arvio_emaxx_reader import ArvioEmaxxReader
        self._state = float(await (getattr(ArvioEmaxxReader(self._endpoint), self._type)()))
