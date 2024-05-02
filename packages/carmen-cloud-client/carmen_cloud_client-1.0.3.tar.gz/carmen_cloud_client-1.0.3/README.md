# Carmen Cloud Client by Adaptive Recognition

Python client for [Carmen Cloud](https://carmencloud.com/) by [Adaptive Recognition](https://adaptiverecognition.com/). This unified library provides you with access to both the **Vehicle API** and the **Transportation & Cargo API**.

## Supported API Versions

- Vehicle API: v1.4.1
- Transportation & Cargo API: v1.0.1

## 🛠️ How to Install

```sh
pip install carmen-cloud-client
```

## 🚀 Usage

You can utilize either the Vehicle API or the Transportation & Cargo API based on your needs.

### 🚗 Vehicle API

```python
from carmen_cloud_client import VehicleAPIClient, VehicleAPIOptions, SelectedServices, Locations

options = VehicleAPIOptions(
    api_key="<YOUR_API_KEY>",
    services=SelectedServices(anpr=True, mmr=True),
    input_image_location=Locations.Europe.Hungary,
    cloud_service_region="EU"
)
client = VehicleAPIClient(options)

response = client.send("./car.jpg")
print(response)
```

### 🚚 Transportation & Cargo API

```python
from carmen_cloud_client import TransportAPIClient, TransportAPIOptions, CodeType

options = TransportAPIOptions(
    api_key="<YOUR_API_KEY>",
    type=CodeType.ISO,
    cloud_service_region="EU"
)
client = TransportAPIClient(options)

response = client.send("./container.jpg")
print(response)
```

## 🔧 Development

For more information about developing and contributing to this project, see [DEVELOPMENT.md](DEVELOPMENT.md).
