from datetime import datetime

class DateConverter:
    regex = '[0-9]{2}-[0-9]{2}-[0-9]{4}'
    
    def to_python(self, value):
        return datetime.strptime(value, '%d-%m-%Y')
    
    def to_url(self, value):
        return value.strftime('%d-%m-%Y')