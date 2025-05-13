module 0x0::AgricultureMonitoring {
 
    use std::string;
    use iota::object::{UID, new};
    use iota::tx_context::TxContext;
 
    public struct SensorData has copy, drop, store {
        sensor_id: u64,
        humidity: u8,
        temperature: u8,
        soil_moisture: u8,
        timestamp: u64,
    }
 
    // Function to log sensor data and return a SensorData object
    public fun log_sensor_data(
        sensor_id: u64,
        humidity: u8,
        temperature: u8,
        soil_moisture: u8,
        timestamp: u64
    ): SensorData {
        SensorData {
            sensor_id,
            humidity,
            temperature,
            soil_moisture,
            timestamp,
        }
    }
 
    // Function to check if a value is within a range (inclusive)
    public fun is_within_range(value: u8, min_value: u8, max_value: u8): bool {
        value >= min_value && value <= max_value
    }
 
    // Function to verify if the timestamp is within a specified range
    public fun is_time_in_range(
        timestamp: u64,
        min_time: u64,
        max_time: u64
    ): bool {
        timestamp >= min_time && timestamp <= max_time
    }
 
    // Function to verify sensor data with ranges for all parameters
    public fun verify_sensor_data_with_ranges(
        data: &SensorData,
        min_humidity: u8,
        max_humidity: u8,
        min_temperature: u8,
        max_temperature: u8,
        min_soil_moisture: u8,
        max_soil_moisture: u8,
        min_time: u64,
        max_time: u64
    ): bool {
        is_within_range(data.humidity, min_humidity, max_humidity) &&
        is_within_range(data.temperature, min_temperature, max_temperature) &&
        is_within_range(data.soil_moisture, min_soil_moisture, max_soil_moisture) &&
        is_time_in_range(data.timestamp, min_time, max_time)
    }
}