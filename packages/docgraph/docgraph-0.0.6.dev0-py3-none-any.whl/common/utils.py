
import csv
from datetime import datetime
import io
import logging
import re
from urllib.parse import urlparse

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By 
import tiktoken
import yaml

log = logging.getLogger(__name__)

TOKENIZER_ENCODING_NAME = "cl100k_base"

def is_pdf(url):
    """Returns True if url is a pdf."""
    # There are some urls that end with pdf but don't have .pdf in the url
    parts = urlparse(url)
    # return '.pdf' in url.lower() or url.lower().endswith('pdf')
    return parts.path.lower().endswith('pdf')


    # return '.pdf' in url.lower() or url.lower().endswith('pdf')

def get_csv_dict_reader_from_s3(ds, csv_file_key):

    # Get csv file from MinIO
    # Example csv file key: pipelines/xlsx/reprocess_documents_missing_28_docs_44_excessive_length.csv
    s3_obj = ds.s3.GetObject(ds.s3def['sets']['documents']['bucket'], csv_file_key)

    # Convert bytes to string
    csv_str = io.TextIOWrapper(io.BytesIO(s3_obj), encoding="utf-8")
    csv_dict_reader = csv.DictReader(csv_str)

    return csv_dict_reader

def get_urls_from_csv(ds, csv_file_key):
    csv_dict_reader = get_csv_dict_reader_from_s3(ds, csv_file_key)
    
    pdfs = {}
    urls = []
    for i, row in enumerate(csv_dict_reader):
        url = row['url']
        if is_pdf(url):
            pdfs[url] = {
                'index': i,
                'parent': row['parent_page'],
            }
        else:
            urls.append(url)

    return pdfs, urls

def get_reprocess_document_query(ds, csv_file_key):
    document_dict_reader = get_csv_dict_reader_from_s3(ds, csv_file_key)

    # Create table in Postgres that will be dropped after reprocessing
    # Ref: https://www.psycopg.org/psycopg3/docs/basic/copy.html
    temp_table_name = f'temp_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    with ds.conn.cursor() as cur:
        cur.execute(f'CREATE TABLE {temp_table_name} (document_id int PRIMARY KEY);')
        log.info(f'Created temporary table: {temp_table_name}')

        # Copy csv file to temporary table
        with cur.copy(f'COPY {temp_table_name} (document_id) FROM STDIN') as copy:
            for row in document_dict_reader:
                row_tuple = (row['document_id'],)
                copy.write_row(row_tuple)


    # Create query to reprocess documents
    query = f"""SELECT {ds.tables['document']}.* FROM {ds.tables['document']}
                INNER JOIN {temp_table_name}
                ON {ds.tables['document']}.document_id = {temp_table_name}.document_id;"""

    return query, temp_table_name
    
# Ref: https://platform.openai.com/docs/guides/embeddings/how-can-i-tell-how-many-tokens-a-string-has-before-i-embed-it
def get_num_tokens_from_string(text, encoding_name):
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(text))
    return num_tokens   

def split_text_up_to_limit(text, token_limit):

    # Check if text is already under limit
    total_tokens = get_num_tokens_from_string(text, TOKENIZER_ENCODING_NAME)
    if total_tokens <= token_limit:
        first_part ={
            'text': text,
            'num_tokens': total_tokens,
            'num_words': len(text.split())
        }

        second_part = {
            'text': '',
            'num_tokens': 0,
            'num_words': 0
        }

        return first_part, second_part

    text_list = re.split('(\W)', text)

    # Loop through words from the end until under or at limit
    first_part_text = ''
    first_part_num_tokens = 0

    # Start from end of list
    for i in range(-1, -len(text_list), -1):
        first_part_text = ''.join(text_list[:i])

        num_tokens = get_num_tokens_from_string(first_part_text, TOKENIZER_ENCODING_NAME)
        if num_tokens <= token_limit:
            # Still under limit 
            first_part_num_tokens = num_tokens
            break

        
    first_part = {
        'text': first_part_text,
        'num_tokens': first_part_num_tokens,
        'num_words': len(first_part_text.split())
    }

    second_part_text = ''.join(text_list[i:])
    second_part = {
        'text': ''.join(second_part_text),
        'num_tokens': get_num_tokens_from_string(second_part_text, TOKENIZER_ENCODING_NAME),
        'num_words': len(second_part_text.split())
    }

    return first_part, second_part

def login(credentials_path=None, creds=None, credentials_name='aig_credentials',
          url_authentication='https://knowledge1.thermofisher.com/Special:UserLogin',
          max_wait_sec=10.0):
    if credentials_path:
        with open(credentials_path, 'r') as yamlfile:
            print('loading credentials...')
            creds = yaml.safe_load(yamlfile)
    elif creds is None:
        raise ValueError('credentials_path or creds must be provided')

    user = None
    password = None
    if creds is not None:
        
        k1_creds = next((x for x in creds['api'] if x['name'] == credentials_name), None)
        if k1_creds is not None:
            user = k1_creds['user']
            password = k1_creds['password']

    if user is None or password is None:
        raise ValueError('user or password not found in credentials file')

    return get_http_session(url_authentication, max_wait_sec, user, password)


def get_http_session(url_authentication, max_wait_sec, user, password):
    session = requests.session()
    # load the webpage content 
    # start by defining the options 
    options = webdriver.ChromeOptions() 
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    payload = {
        'username': user,
        'password': password,
        'returntotitle': None, 
        'returnquery': None, 
        'deki_buttons[action][login]': 'login',
        }


    driver.get(url_authentication)
    driver.find_element(By.ID, "text-username").send_keys(user)
    driver.find_element(By.ID, "password-password").send_keys(password)
    driver.find_element(By.NAME,'deki_buttons[action][login]').click()
    driver.implicitly_wait(max_wait_sec)

    login_req = session.post(url_authentication, data=payload)
    print(f'Login status_code: {login_req.status_code}')
    if login_req.status_code != 200:
        raise ValueError('Login failed')

    return driver, session



