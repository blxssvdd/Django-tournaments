from django.shortcuts import render

# Create your views here.


def index(request):
    context = {
        "tournaments": [
            {
                "name": "Турнір 1",
                "count": 5,
                "date": "2023-10-01",
                "players": 20
            },
            {
                "name": "Турнір 2",
                "count": 3,
                "date": "2023-10-15",
                "players": 15
            },
            {
                "name": "Турнір 3",
                "count": 4,
                "date": "2023-11-01",
                "players": 25
            }
        
    ]}
    return render(request=request, template_name="index.html", context=context)