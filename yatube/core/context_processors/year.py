from datetime import datetime

def year(request):
    current_date = datetime.now().date()
    return {
        'year':(current_date.year),
    }