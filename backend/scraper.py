import subprocess
import json
import os
import tempfile
from config import get_config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ── MCP CONFIG HELPERS ───────────────────────────────────────────────────────────

def create_mcp_config(api_token, web_unlocker_zone=None, browser_auth=None):
    """Create a temporary MCP configuration file with Bright Data settings."""
    config = {
        'mcpServers': {
            'Bright Data': {
                'command': 'npx',
                'args': ['@brightdata/mcp'],
                'env': {'API_TOKEN': api_token}
            }
        }
    }
    if web_unlocker_zone:
        config['mcpServers']['Bright Data']['env']['WEB_UNLOCKER_ZONE'] = web_unlocker_zone
    if browser_auth:
        config['mcpServers']['Bright Data']['env']['BROWSER_AUTH'] = browser_auth
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    json.dump(config, tmp)
    tmp.close()
    return tmp.name


def run_mcp_scraper(prompt, config_path):
    """Run a Bright Data MCP scraping task and return parsed results."""
    try:
        cmd = ['npx', '@brightdata/mcp-client', '--config', config_path, '--prompt', prompt]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f'MCP client error: {result.stderr}')
            return []
        for line in result.stdout.strip().split('\n'):
            line = line.strip()
            if line.startswith('{') and line.endswith('}'):
                try:
                    data = json.loads(line)
                    if 'agents' in data:
                        return data['agents']
                    return [data]
                except json.JSONDecodeError:
                    continue
        return []
    except Exception as e:
        logger.error(f'Error running MCP client: {e}')
        return []
    finally:
        if os.path.exists(config_path):
            os.unlink(config_path)


# ── CARE HOME SCRAPER (Sussex Staffing Solutions) ─────────────────────────────────

def scrape_care_homes(location='Sussex, UK', limit=30):
    """
    Scrape CQC-registered care homes in the target area using Bright Data MCP.
    Falls back to dummy data if no API key is set.
    """
    config = get_config()
    api_token = config.get('BRIGHTDATA_API_TOKEN', '')
    web_unlocker_zone = config.get('BRIGHTDATA_WEB_UNLOCKER_ZONE', '')
    browser_auth = config.get('BRIGHTDATA_BROWSER_AUTH', '')

    if not api_token:
        logger.warning('No Bright Data API token — using dummy care home data.')
        return generate_dummy_care_homes(location, limit)

    config_path = create_mcp_config(api_token, web_unlocker_zone, browser_auth)
    prompt = (
        f'Extract data for {limit} CQC-registered care homes in {location} '
        f'from https://www.cqc.org.uk/search?query=care+home&location={location}. '
        f'For each home get: name, phone number, address, type (nursing home or residential), '
        f'number of beds, manager name if available. Return as structured JSON.'
    )
    raw = run_mcp_scraper(prompt, config_path)
    results = []
    for item in raw[:limit]:
        name = item.get('name', 'Unknown Care Home')
        category = 'Nursing Home' if 'nurs' in name.lower() else 'Residential Care Home'
        priority = 'HIGH' if category == 'Nursing Home' else 'MEDIUM'
        results.append({
            'name': name,
            'phone': item.get('phone', 'N/A'),
            'category': category,
            'address': item.get('address', location),
            'website': item.get('website', ''),
            'priority': priority,
            'buyer_count': 0
        })
    return results


def generate_dummy_care_homes(location='Sussex, UK', limit=30):
    """Dummy care home data for testing without API keys."""
    home_types = [
        ('Sunrise Nursing Home', 'Nursing Home', 'HIGH'),
        ('Seaview Residential', 'Residential Care Home', 'MEDIUM'),
        ('Brighton Care Centre', 'Nursing Home', 'HIGH'),
        ('Sussex Manor', 'Residential Care Home', 'MEDIUM'),
        ('Eastbourne Nursing Lodge', 'Nursing Home', 'HIGH'),
    ]
    dummy = []
    for i in range(limit):
        t = home_types[i % len(home_types)]
        dummy.append({
            'name': f'{t[0]} {i + 1}',
            'phone': f'01273 55{1000 + i}',
            'category': t[1],
            'address': f'{100 + i} High Street, {location}',
            'website': '',
            'priority': t[2],
            'buyer_count': 0
        })
    return dummy


# ── ROOFING LEAD SCRAPER ─────────────────────────────────────────────────────────────

def scrape_roofing_leads(location='Brighton, UK', limit=30):
    """
    Scrape homeowner/roofing leads via Google Maps using Bright Data MCP.
    Falls back to dummy data if no API key is set.
    """
    config = get_config()
    api_token = config.get('BRIGHTDATA_API_TOKEN', '')
    web_unlocker_zone = config.get('BRIGHTDATA_WEB_UNLOCKER_ZONE', '')
    browser_auth = config.get('BRIGHTDATA_BROWSER_AUTH', '')

    if not api_token:
        logger.warning('No Bright Data API token — using dummy roofing data.')
        return generate_dummy_roofing_leads(location, limit)

    config_path = create_mcp_config(api_token, web_unlocker_zone, browser_auth)
    prompt = (
        f'Find {limit} residential properties or homeowners in {location} '
        f'who may need roofing services. Search Google Maps for '
        f'"houses {location}" and extract: address, postcode, any contact info. '
        f'Also search local Facebook groups for posts mentioning roof damage, '
        f'leaks, or roofing work in {location}. Return as structured JSON.'
    )
    raw = run_mcp_scraper(prompt, config_path)
    results = []
    for item in raw[:limit]:
        results.append({
            'name': item.get('name', 'Homeowner'),
            'phone': item.get('phone', 'N/A'),
            'category': 'Roofing Lead',
            'address': item.get('address', location),
            'website': '',
            'priority': 'MEDIUM',
            'buyer_count': 0
        })
    return results


def generate_dummy_roofing_leads(location='Brighton, UK', limit=30):
    """Dummy roofing lead data for testing without API keys."""
    issues = ['Roof leak', 'Storm damage', 'Missing tiles', 'Flat roof repair', 'Guttering']
    dummy = []
    for i in range(limit):
        dummy.append({
            'name': f'Homeowner {i + 1}',
            'phone': f'07700 90{1000 + i}',
            'category': 'Roofing Lead',
            'address': f'{10 + i} Church Road, {location}',
            'website': '',
            'priority': 'MEDIUM',
            'issue': issues[i % len(issues)],
            'buyer_count': 0
        })
    return dummy


# ── MAIN ENTRY POINT (keeps backward compat with app.py) ───────────────────────────

def scrape_real_estate_leads(location='Sussex, UK', limit=30, mode='sussex_staffing'):
    """
    Main scraping entry point.
    mode: 'sussex_staffing' (care homes) or 'roofing' (homeowners).
    Keeps the original function name so app.py doesn't need changing.
    """
    if mode == 'roofing':
        return scrape_roofing_leads(location, limit)
    return scrape_care_homes(location, limit)
