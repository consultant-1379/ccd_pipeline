kubectl patch svc kubernetes -p '{"spec": {"ports": [{"port": 443,"targetPort": 443,"name": "https"}],"type": "LoadBalancer"}}'
