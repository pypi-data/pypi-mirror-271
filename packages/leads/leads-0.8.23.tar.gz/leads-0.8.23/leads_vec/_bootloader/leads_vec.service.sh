if [ ! -x "/usr/local/leads/config.json" ];
then
  echo "Error: Config file does not exist"
  exit 1
fi
python3.12 -m leads_vec -c /usr/local/leads/config.json --xws run