import requests
from bs4 import BeautifulSoup

def getSession(schoolid: str, user: str, pwd: str) -> requests.Session:
    '''
    Get a requests.Session logged in to lectio.dk

    Get a Session logged in to lectio.dk with username `user` and
    password `pwd` in school `schoolid`

    Parameters
    ----------
    schoolid : str
        Id of the institution
    user : str
        User login name
    pwd : str
        User login password

    Raises
    ------
    ConnectionError
        If a non 200 response code is received

    Returns
    -------
    requests.Session
        A logged in Session
    ''' 

    url = f'https://www.lectio.dk/lectio/{schoolid}/login.aspx'

    # Fake browser user agent
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3424.0 Safari/537.36'
    headers = {'User-agent':user_agent}

    s = requests.Session()
    s.headers = headers

    # Get login page
    r = s.get(url)

    if not r.ok:
        raise ConnectionError(f'Non 200 response code returned from {url}')

    # Extract all hidden input values
    soup = BeautifulSoup(r.content, 'html.parser')
    hidden = soup.find_all('input', {'type':'hidden'})

    # At the time of making this, `target` will be equal to `url`, but if lectio changes so will this
    target = 'https://www.lectio.dk/lectio/680' + soup.find('form', {'method':'post'})['action'].strip('.')

    # Payload is the HTTPS request body
    payload = dict()

    # Add elements from the list `hidden` to the dict `payload` 
    for inp in hidden:
        payload[inp['name']] = inp.get('value', '')

    # Add login creds to `payload`
    payload['m$Content$username2'] = user
    payload['m$Content$passwordHidden'] = pwd

    # Set event target, which is the id of the login button
    payload['__EVENTTARGET'] = 'm$Content$submitbtn2'

    # Required in the HTTPS post
    payload['__EVENTARGUMENT'] = ''
    payload['LectioPostbackId'] = ''

    # query is not required, but del might be overkill
    del payload['query']

    # Post login creds
    r = s.post(target, data=payload, headers=headers)

    if not r.ok:
        raise ConnectionError(f'Non 200 response code returned from {url} when posting login credentials')

    # Return logged in session
    return s