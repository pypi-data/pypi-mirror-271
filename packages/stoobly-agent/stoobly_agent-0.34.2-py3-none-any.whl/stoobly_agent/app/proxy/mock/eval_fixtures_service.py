import os
import pdb
import re

from io import BytesIO
from mitmproxy.http import Request as MitmproxyRequest
from requests import Response
from typing import Union

from stoobly_agent.lib.logger import bcolors, Logger

from .types import Fixtures

class Options():
  public_directory_path: str
  response_fixtures: Fixtures

def eval_fixtures(request: MitmproxyRequest, **options: Options) -> Union[Response, None]:
  response_fixtures = options.get('response_fixtures')

  fixture_path = __eval_response_fixtures(request, response_fixtures)
  if not fixture_path:
    public_directory_path = options.get('public_directory_path')

    if public_directory_path and os.path.exists(public_directory_path):
      static_file_path = os.path.join(public_directory_path, request.path.lstrip('/'))

      if os.path.exists(static_file_path):
        fixture_path = static_file_path

  if not fixture_path:
    return

  with open(fixture_path, 'rb') as fp:
    response = Response()

    response.status_code = 200
    response.raw = BytesIO(fp.read()) 

    Logger.instance().debug(f"{bcolors.OKBLUE}Resolved fixture {fixture_path}{bcolors.ENDC}")

    return response

def __eval_response_fixtures(request: MitmproxyRequest, response_fixtures: Fixtures):
  if not response_fixtures:
    return

  method = request.method
  routes = response_fixtures.get(method)

  if not routes:
    return

  for path_pattern in routes:
    if not re.match(path_pattern, request.path):
      continue
    
    path = routes[path_pattern].get('path')

    if path and os.path.exists(path):
      return path