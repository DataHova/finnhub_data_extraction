import os
from dotenv import load_dotenv

load_dotenv()

# SECURED CONNECTION TO THE HOST
bootstrap_servers = os.getenv("BOOTSTRAP_SERVER")
finnhub_api_key = os.getenv('FINNHUB_API_KEY')

# KAFKA PARAMETERS
topic = os.getenv('topic')
group_id = os.getenv('groupid')
auto_offset_reset_earliest = os.getenv('auto_offset_reset_earliest')
auto_offset_reset_latest = os.getenv('auto_offset_reset_latest')