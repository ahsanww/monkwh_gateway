dummy_data = [
    {
        "index": i + 1,
        "kwh": 1000.0 + i,
        "kvarh": 200.0 + i,
        "kw": 10.0 + (i * 0.1),
        "kva": 12.0 + (i * 0.1),
        "pf": 0.95,
        "voltage_l1": 230.0,
        "voltage_l2": 231.0,
        "voltage_l3": 232.0,
        "current_l1": 5.0,
        "current_l2": 5.1,
        "current_l3": 5.2,
        "event": "none",
    }
    for i in range(96)
]

# print(dummy_data)
cooked_data = {
    "id_pelanggan": 1,
    "meterSerialNumber": 2,
    "date": "25-11-2025",
    "dataIndex": 96,
    "data": dummy_data,
    "status": 200,
    "error": "none",
}
print(cooked_data)
