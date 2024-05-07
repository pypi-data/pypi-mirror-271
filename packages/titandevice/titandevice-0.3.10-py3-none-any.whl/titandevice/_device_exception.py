class TitanException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class DeviceNoFoundException(TitanException):
    def __init__(self, device_serial):
        super().__init__(f"Device with serial {device_serial} not found")


class DeviceMustBeRootedException(TitanException):
    def __init__(self, device_serial):
        super().__init__(
            f'Device [{device_serial}] must be rooted to perform this operation'
        )


class FridaServerNotInstalledException(TitanException):
    def __init__(self, device_serial, frida_server_path):
        super().__init__(
            f'Frida server is not installed in {frida_server_path} on device with serial {device_serial}'
        )


class FridaServerNotRunningException(TitanException):
    def __init__(self, device_serial, frida_server_name):
        super().__init__(
            f'Frida server [{frida_server_name}] is not running on device with serial {device_serial}'
        )


class PackageNotInstalledException(TitanException):
    def __init__(self, device_serial, package_name):
        super().__init__(f'Package {package_name} is not installed in {device_serial}')


class InstallPackageMustUninstallFirstException(TitanException):
    def __init__(self, device_serial, package_name):
        super().__init__(
            f'Package {package_name} is already installed in {device_serial}'
        )
