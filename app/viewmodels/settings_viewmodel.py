from app.models.storage_manager import StorageManager


class SettingsViewModel:
    def __init__(self, storage: StorageManager):
        self.storage = storage

    def get_notifications_enabled(self) -> bool:
        val = self.storage.get_setting('notifications_enabled', 'True')
        return val == 'True'

    def set_notifications_enabled(self, enabled: bool):
        self.storage.set_setting('notifications_enabled', str(enabled))

    def export_data(self, file_path: str):
        self.storage.export_data(file_path)
