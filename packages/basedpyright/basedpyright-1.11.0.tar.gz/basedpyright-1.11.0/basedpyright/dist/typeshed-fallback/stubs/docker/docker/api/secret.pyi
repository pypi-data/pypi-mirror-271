from _typeshed import Incomplete

class SecretApiMixin:
    def create_secret(self, name, data, labels: Incomplete | None = None, driver: Incomplete | None = None): ...
    def inspect_secret(self, id): ...
    def remove_secret(self, id): ...
    def secrets(self, filters: Incomplete | None = None): ...
