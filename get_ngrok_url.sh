#!/bin/bash
# get_ngrok_url.sh

echo $(curl -s $(docker port jobie-app-ngrok 4040)/api/tunnels | grep -P "http://.*?ngrok.io" -oh)
