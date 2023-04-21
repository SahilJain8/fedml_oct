from django.shortcuts import render
from django.http import HttpResponse
import flwr as fl


# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request, "index.html")
    else:
        return HttpResponse("Invalid request")


import threading
import flwr

from django.shortcuts import render
from django.views import View


class FLwrView(View):
    template_name = 'flwr.html'

    def get(self, request):
       
        t = threading.Thread(target=self.start_flwr_server)
        t.start()


        context = {'message': 'FLwr server started'}
        return render(request, self.template_name, context)

    def start_flwr_server(self):
        strategy = flwr.server.strategy.FedAvg(min_num_clients=1)
        flwr.server.start_server(server_address="0.0.0.0:8080", config=flwr.server.ServerConfig(num_rounds=3),strategy=strategy)
        
