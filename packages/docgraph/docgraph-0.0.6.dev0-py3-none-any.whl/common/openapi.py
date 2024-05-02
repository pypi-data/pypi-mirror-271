from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type
import numpy as np
import asyncio
import openai
from openai import OpenAI, AzureOpenAI, AsyncOpenAI, AsyncAzureOpenAI
import time
from copy import copy, deepcopy
import yaml
import tiktoken
import logging

token_limits =  {
                    'tstgpt35t':8193,
                    'gpt-35-turbo':4096,
                    'gpt-35-turbo-16k':16384,
                    'gpt-35-turbo-0301': 8192,
                    'text-davinci-003':4097,
                    'text-embedding-ada-002': 8192,
                    'text-embedding-ada-002_v1': 4095,
                    'gpt-35-turbo-1106': 16384,
                    'gpt-4': 4095,
                    'gpt-4-32k': 32768,
                    'gpt-4-1106': 16385,
                    'gpt-4-vision': 128000,
                }

@retry(wait=wait_random_exponential(max=5), 
       stop=stop_after_attempt(3), 
       retry=retry_if_exception_type((openai.APIError, openai.Timeout)), 
       reraise=True)
def compute_embedding(text, engine="text-embedding-ada-002_v1"):
    if not isinstance(text, list):
        text = [text]
    # replace newlines, which can negatively affect performance.
    results = openai.Embedding.create(input=text, engine=engine)
    return results

@retry(wait=wait_random_exponential(max=5), 
       stop=stop_after_attempt(3), 
       retry=retry_if_exception_type((openai.APIError, openai.Timeout)), 
       reraise=True)
def compute_completion(prompt, engine="tstgpt35t", temperature=1.0, max_tokens=512 ):
    response = openai.Completion.create(
            engine=engine,
            prompt= prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
    return response

@retry(wait=wait_random_exponential(max=5), 
       stop=stop_after_attempt(3), 
       retry=retry_if_exception_type((openai.APIError, openai.Timeout, TimeoutError)), 
       reraise=True)
def list_models():
    response = openai.Model.list_models()
    return response

def CheckKeys(key, dict, source = None):
    if key not in dict:
        err_msg = '{} not in {}'.format(key, dict.keys())
        if source is not None:
            err_msg += ' from' + source
        log.error(err_msg)
        raise Exception(err_msg)

def EstimateTokens(text, scale = 3.0): # Be conservative on token count if hitting the token limit results in failure
    return int((scale+len(text)-1)/scale) 

def CountTokens(text, model="gpt-3.5-turbo"):
    
    if model == "tstgpt35t" or 'gpt-35' in model:    #translate to model name compatible with tiktoken
        model = "gpt-3.5-turbo"
    
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = len(encoding.encode(text))
    return num_tokens

class openapi(object):
    def __init__(self,
                 text_engine="text-embedding-ada-002_v1", 
                 match_engine="text-embedding-ada-002_v1", 
                 creds= None, 
                 completions_engine="gpt-35-turbo", 
                 resources = None):

        if resources is None or len(resources) == 0:
            resources = []
            for api in creds['api']:
                if 'name' in api and 'url' in api and 'key' in api and 'api_type' in api and 'api_version' in api:
                    resources.append(api['name'])

        self.text_engine = text_engine
        self.match_engine = match_engine
        self.completions_engine = completions_engine
        self.resources = {}
        self.available_models = {}
        self.rate_limited_models = {}
        if creds != None:
            for resource in resources:
                resource_creds = next((x for x in creds['api'] if x['name'] == resource), None)
                if resource_creds:
                    self.resources['resource'] = resource_creds
                    if 'models' in resource_creds and resource_creds['models'] != None and len(resource_creds['models']) > 0:
                        for model in resource_creds['models']:
                            model_resources = deepcopy(model)
                            model_resources['name'] = resource_creds['name']
                            model_resources['url'] = resource_creds['url']
                            model_resources['key'] = resource_creds['key']
                            model_resources['key2'] = resource_creds['key2']
                            model_resources['region'] = resource_creds['region']
                            model_resources['api_type'] = resource_creds['api_type']
                            model_resources['api_version'] = resource_creds['api_version']
                            if 'context_tokens' in model:
                                model_resources['context_tokens'] = model['context_tokens']
                            if 'completion_tokens' in model:
                                model_resources['completion_tokens'] = model['completion_tokens']

                            model_resources['client'] =  self.oai_client(model_resources)
                            model_resources['async_client'] = self.async_oai_client(model_resources)
                            model_resources['use'] = []
                            if model['name'] not in self.available_models:
                                self.available_models[model['name']] = [model_resources]
                                self.rate_limited_models[model['name']]=[]
                            else:
                                self.available_models[model['name']].append(model_resources) 
        # if self.completions_engine in self.available_models and len (self.available_models[self.completions_engine]) > 0:
        #     self.set_creds(self.available_models[self.completions_engine][0])

    def CountTokens(self, text, model="gpt-3.5-turbo"):
        return CountTokens(text, model)


    def oai_client(self, api_cred):
        client = None
        if api_cred['api_type'] == 'azure':
            client = AzureOpenAI(api_key=api_cred['key'], api_version = api_cred['api_version'], azure_endpoint = api_cred['url'])
        else: # OpenAI credentials
            client = OpenAI(api_key=api_cred['key'])
        return client
    
    def async_oai_client(self, api_cred):
        client = None
        if api_cred['api_type'] == 'azure':
            client = AsyncAzureOpenAI(api_key=api_cred['key'], api_version = api_cred['api_version'], azure_endpoint = api_cred['url'], timeout=30)
        else: # OpenAI credentials
            client = AsyncOpenAI(api_key=api_cred['key'])
        return client


    # def set_creds(self, api_cred):
    #     if api_cred['api_type'] == 'azure':
    #         self.client = AsyncOpenAI(
    #             api_key=api_cred['key'],
    #             api_type=api_cred['api_type'],
    #             api_base=api_cred['url'],
    #             api_version=api_cred['api_version']
    #         )
    #     else: # OpenAI credentials
    #         self.client = AsyncOpenAI(api_key=api_cred['key'])

    def PopModel(self, call_tokens, model_name = 'text-embedding-ada-002_v1'):
        use_model = None

        if model_name in self.available_models:
            tic = time.perf_counter()
            for i, model in enumerate(self.available_models[model_name]):
                unused_tokens = model['rate_limit']
                for use in model['use']:
                    if tic-use['timestamp'] < 60:
                        unused_tokens -= use['tokens']
                    else:
                        model['use'].remove(use)
                if unused_tokens > call_tokens:
                    break
                else:
                    self.available_models[model_name].append(self.available_models[model_name].pop(i)) # Push to end
            use_model = self.available_models[model_name].pop(i)
            self.available_models[model_name].append(use_model) # Push to end of queue
        return use_model

    def PeekModel(self, model_name = 'text-embedding-ada-002_v1'):
        use_model = None

        if model_name in self.available_models:
            actual_model = self.available_models[model_name][0]
            use_model = {'name': actual_model['name'], 'model_name': actual_model['model_name'], 'rate_limit': actual_model['rate_limit']}
            if 'context_tokens' in actual_model:
                use_model['context_tokens'] = actual_model['context_tokens']
            if 'completion_tokens' in actual_model:
                use_model['completion_tokens'] = actual_model['completion_tokens']

        return use_model

    @retry(wait=wait_random_exponential(max=5), 
        stop=stop_after_attempt(5), 
        retry=retry_if_exception_type((openai.APIError, openai.Timeout, TimeoutError)), 
        reraise=True)
    def embedding(self, text, model_name = None, timeout=3):
        dt = 0
        if model_name == None:
            model_name = self.match_engine

        embedding_vector = None
        if isinstance(text, str) and len(text.strip()) > 0 and model_name in self.available_models:
            call_tokens = EstimateTokens(text)
            use_model = self.PopModel(call_tokens, model_name)
            if use_model is not None:
                # self.set_creds(use_model)
                tic = time.perf_counter()
                text_embedding = use_model['client'].embeddings.create(input=text, model=use_model['deployment_name'], timeout=timeout)
                toc = time.perf_counter()
                dt = toc - tic
                embedding_vector = text_embedding.data[0].embedding
                use_model['use'].append({'timestamp': tic, 'dt': dt, 'tokens': text_embedding.usage.total_tokens})
                print(f"embedding Successful {use_model['name']} {use_model['model_name']}, dt:{dt}, total_tokens: {text_embedding.usage.total_tokens}") 

        return embedding_vector

    @retry(wait=wait_random_exponential(max=5), 
        stop=stop_after_attempt(3), 
        retry=retry_if_exception_type((openai.APIError, openai.Timeout, TimeoutError)), 
        reraise=True)
    async def AsyncEmbedding(self, text, model_name = None, timeout=3):
        dt = 0
        if model_name == None:
            model_name = self.match_engine

        embedding_vector = None
        if model_name in self.available_models:
            call_tokens = EstimateTokens(text)
            use_model = self.PopModel(call_tokens, model_name)
            if use_model is not None:
                # self.set_creds(use_model)
                tic = time.perf_counter()
                text_embedding = await use_model['async_client'].embeddings.create(input=text, model=use_model['deployment_name'], timeout=timeout)
                #text_embedding = compute_embedding(text, engine = self.match_engine)
                toc = time.perf_counter()
                dt = toc - tic
                embedding_vector = text_embedding.data[0].embedding
                use_model['use'].append({'timestamp': tic, 'dt': dt, 'tokens': text_embedding.usage.total_tokens})
                print(f"embedding Successful {use_model['name']} {use_model['model_name']}, dt:{t}, total_tokens: {text_embedding.usage.total_tokens}")

        return embedding_vector

    def match(self, text, embeddings, model = 'text-embedding-ada-002_v1'):
        text = text.replace("\n", " ")
        embedding, dt = embedding(text, engine = self.match_engine)

        match_dot = []
        for text_embedding in enumerate(embeddings):
            dot_product = np.dot(text_embedding, embedding)
            match_dot.append(dot_product.item())

        iMax = match_dot.index(max(match_dot))

        return iMax, match_dot, dt
    
    @retry(wait=wait_random_exponential(max=5), 
        stop=stop_after_attempt(3), 
        retry=retry_if_exception_type((openai.APIError, openai.Timeout, TimeoutError)), 
        reraise=True)
    def completion(self, prompt, engine='gpt-35-turbo-0301', temperature=0.1, max_tokens=2048, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0, stop=["<|im_end|>"], call_tokens = None):
        response_dict = None
        if engine == None:
            engine = self.match_engine

        if engine in self.available_models:
            if call_tokens == None:
                call_tokens = token_limits[engine]
            use_model = self.PopModel(call_tokens, engine)
            if use_model is not None:
                if 'completion_tokens' in use_model:
                    max_tokens = min(max_tokens, use_model['completion_tokens'])

                tic = time.perf_counter()
                response = use_model['client'].completions.create(
                    model=use_model['deployment_name'],
                    prompt= prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                    stop=stop
                )
                toc = time.perf_counter()

                response_dict = {
                    'model': response.model,
                    'usage': {'completion_tokens': response.usage.completion_tokens, 'prompt_tokens': response.usage.prompt_tokens, 'total_tokens': response.usage.total_tokens},
                    'dt': toc - tic,
                    'messages': [],
                }
                for choice in  response.choices:
                    response_dict['messages'].append({'text': choice.text, 'finish_reason': choice.finish_reason})

                print(f"completion Successful {use_model['name']} {use_model['model_name']}, dt:{response_dict['dt']}, total_tokens: {response_dict['usage']['total_tokens']}") 


        return response_dict
    
    # https://platform.openai.com/docs/api-reference/chat
    @retry(wait=wait_random_exponential(max=5), 
        stop=stop_after_attempt(3), 
        retry=retry_if_exception_type((openai.APIError, openai.Timeout, TimeoutError)), 
        reraise=True)
    def ChatCompletion(self, messages, engine=None, response_format=None, temperature=0.1, max_tokens=None, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0, call_tokens = None, timeout=30.0):
        response_dict = None
        if engine == None:
            engine = self.completions_engine

        if engine in self.available_models:
            if call_tokens == None:
                call_tokens = token_limits[engine]
            use_model = self.PopModel(call_tokens, engine)
            if use_model is not None:
                if max_tokens is None:
                    max_tokens = use_model['completion_tokens']
                else:
                    max_tokens = min(max_tokens, use_model['completion_tokens'])
                    
                try:
                    tic = time.perf_counter()
                    response = use_model['client'].chat.completions.create(
                        messages=messages,
                        model=use_model['deployment_name'],
                        temperature=temperature,
                        max_tokens=max_tokens,
                        top_p=top_p,
                        frequency_penalty=frequency_penalty,
                        presence_penalty=presence_penalty,
                        timeout=timeout,
                    )
                    toc = time.perf_counter()

                    response_dict = {
                        'model': response.model,
                        'finish_reason': response.choices[0].finish_reason,
                        'dt': toc - tic,
                        'text': response.choices[0].message.content,
                    }
                    if response.usage is not None:
                        response_dict['usage'] = {'completion_tokens': response.usage.completion_tokens, 'prompt_tokens': response.usage.prompt_tokens, 'total_tokens': response.usage.total_tokens}
                    if response_dict['finish_reason'] == 'content_filter' and response_dict['text'] is None:
                        filter_results = yaml.dump(response.prompt_filter_results[0]['content_filter_results'], indent=2, sort_keys=False)
                        response_dict['text'] = f'Finish reason: {response.choices[0].finish_reason}  Details:\n{filter_results}'
                    print(f"ChatCompletion finish_reason={response_dict['finish_reason']} {use_model['name']} {use_model['model_name']}, dt:{response_dict['dt']}") 

                except Exception as error:
                    toc = time.perf_counter()
                    print(f"Exception {type(error)}: failed to complete chat {use_model['name']} {use_model['deployment_name']}, dt:{toc - tic}.  {error}")
                    raise error
        else:
            response_dict = {'engine': engine, 'error': f"Engine {engine} not available."}

        return response_dict
    
    # https://platform.openai.com/docs/api-reference/chat
    @retry(wait=wait_random_exponential(max=5), 
        stop=stop_after_attempt(3), 
        retry=retry_if_exception_type((openai.APIError, openai.Timeout, TimeoutError)), 
        reraise=True)
    async def AsyncChatCompletion(self, messages, engine=None, temperature=0.1, max_tokens=int(token_limits['gpt-35-turbo']/2), 
                                  top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0, call_tokens = None, timeout=15.0):
        response_dict = None
        if engine == None:
            engine = self.completions_engine

        if engine in self.available_models:
            if call_tokens == None:
                call_tokens = token_limits[engine]
            use_model = self.PopModel(call_tokens, engine)
            if use_model is not None:
                if 'completion_tokens' in use_model:
                    max_tokens = min(max_tokens, use_model['completion_tokens'])
                try:
                    tic = time.perf_counter()
                    # response = await asyncio.wait_for(use_model['async_client'].chat.completions.create(
                    response = await use_model['async_client'].chat.completions.create(
                        messages=messages,
                        model=use_model['deployment_name'],
                        temperature=temperature,
                        max_tokens=max_tokens,
                        top_p=top_p,
                        frequency_penalty=frequency_penalty,
                        presence_penalty=presence_penalty,
                        timeout=timeout,
                    )
                    toc = time.perf_counter()
                except Exception as error:
                    toc = time.perf_counter()
                    print(f"Exception {type(error)}: failed to complete chat {use_model['name']} {use_model['deployment_name']}, dt:{toc - tic}.  {error}")
                    raise error
                response_dict = {
                    'model': response.model,
                    'usage': {'completion_tokens': response.usage.completion_tokens, 'prompt_tokens': response.usage.prompt_tokens, 'total_tokens': response.usage.total_tokens},
                    'finish_reason': response.choices[0].finish_reason,
                    'dt': toc - tic,
                    'text': response.choices[0].message.content,
                }
                print(f"AsyncChatCompletion Successful {use_model['name']} {use_model['deployment_name']}, dt:{response_dict['dt']}, total_tokens: {response_dict['usage']['total_tokens']}")

        return response_dict

    # https://platform.openai.com/docs/api-reference/models/list
    def list_models(self):
        tic = time.perf_counter()
        response = list_models()
        toc = time.perf_counter()

        return response, toc-tic