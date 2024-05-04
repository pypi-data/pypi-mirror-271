from pathlib import Path
import json

class Settings:
    def __init__(self, **kwargs):
        profile=kwargs.pop('profile', "")
        dir = kwargs.pop('dir', '~')
        if dir in ['~', None]:
            dir = Path.home()
        else:
            dir = Path(dir)
        self.file = dir / f".{profile}_settings"

        old_settings = self.read()

        self._settings = {}

        for k,v in kwargs.items():
            if v is None:
                v = old_settings.get(k, None)
            self._settings[k] = v
            setattr(self, k, v)

        self.write(self._settings)

    def read(self):
        if self.file.is_file():
            content = self.file.read_text()
        else:
            content = "{}"
        return json.loads(content)

    def write(self, settings):
        self.file.write_text(json.dumps(settings))

    def dict(self):
        return self._settings
