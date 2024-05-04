from urllib.parse import urlparse
from urllib.request import urlopen
from typing import Optional
from qcodes.instrument import Instrument
import qcodes.validators as vals

class RCDAT_8000_90(Instrument):

    def __init__(self, name      : str, 
                 url             : Optional[str] = "http://192.168.0.109/",
                 **kwargs):

        super().__init__(name = name, **kwargs)

        self._raw_url = url
        self._url = self._validate_url(url)

        self.add_parameter(
            'attenuation',
            get_cmd      = lambda cmd='ATT?': self._get_value(cmd),
            get_parser   = float,
            set_cmd      = lambda value, cmd='SETATT': self._set_value(cmd, value),
            set_parser   = float,
            vals         = vals.Numbers(0, 95),
            label        = 'Attenuation Power',
            unit         = 'dB'
        )
        
        self.connect_message()        

    def get_idn(self):
        mn = self._get_value('MN?').strip('MN=')
        sn = self._get_value('SN?').strip('SN=')
        idn = {'vendor': 'Mini-Circuits', 'model': mn, 'serial': sn, 'firmware': None}
        return idn

    def _validate_url(self, url: str):
        parse_result = urlparse(url)
        assert parse_result.scheme == 'http', 'Scheme of the url must be "http".'
        if parse_result.path in ['/', '']:
            if parse_result.path == '':
                url = f'{url}/'
        else:
            raise ValueError('Path of the url must be either "/" or empty. Example url: "http://192.168.0.109/".')

        return url

    def _get_value(self, cmd: str):
        if not cmd.endswith('?'):
            raise ValueError(f'The command passed ({cmd}) must end with a "?".')

        http_result = urlopen(f'{self._url}:{cmd}', timeout=2)
        byte_result = http_result.read()
        string_result = byte_result.decode()
        return string_result
    
    def _set_value(self, cmd: str, value: Optional[float]):
        cmd = f'{cmd}={value}'
        http_result = urlopen(f'{self._url}:{cmd}', timeout=2)
        byte_result = http_result.read()
        string_result = byte_result.decode()
        
        if string_result == '0':
            raise ValueError('The set command was unsuccessful and the instrument returned an error.')