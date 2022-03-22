from django.db import models
import base64

class SeparatedValuesField(models.TextField):

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        super(SeparatedValuesField, self).__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if not value: return
        if isinstance(value, list):
            return value
        if value == 'NULL': return []

        return list(map(lambda x: str(base64.b64decode(x), 'utf-8'), value.split(self.token)))

    def get_db_prep_value(self, value, connection, prepared=False):
        if not value: return 'NULL'
        assert(isinstance(value, list) or isinstance(value, tuple))
        return self.token.join([str(base64.b64encode(bytes(str(s), 'utf-8')), 'utf-8') for s in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

class DictField(models.TextField):
    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        self.key_val_token = kwargs.pop('key_val_token', ':')
        super(DictField, self).__init__(*args, **kwargs)
    
    def to_b64(self, x):
        return str(base64.b64encode(bytes(str(x), 'utf-8')), 'utf-8')
    def from_b64(self, x):
        return str(base64.b64decode(x), 'utf-8')

    def from_db_value(self, value, expression, connection):
        if isinstance(value, dict): return value
        if value == 'NULL': return {}
        return {
            self.from_b64(o.split(self.key_val_token)[0])
                :
            self.from_b64(o.split(self.key_val_token)[1])
            for o in value.split(self.token)
        }
    
    def get_db_prep_value(self, value, connection, prepared=False):
        if not value: return 'NULL'
        assert isinstance(value, dict)
        return super().get_db_prep_value(self.token.join([f'{self.to_b64(o)}{self.key_val_token}{self.to_b64(value[o])}' for o in value]), connection, prepared)
