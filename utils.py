from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from flask import current_app, request_finished, request_started, request_tearing_down


def send_get_request(url, params=None):
  """
  Sends a GET request to the specified URL with optional parameters.

  Args:
    url (str): The URL to send the request to.
    params (dict, optional): A dictionary of query parameters. Defaults to None.

  Returns:
    requests.Response: The response object from the server.
  """
  try:
    response = request_started.get(url, params=params)
    response.raise_for_status()  # Raise an exception for non-2xx status codes
    return response
  except REQUESTED_RANGE_NOT_SATISFIABLE.exceptions.RequestException as e:
    current_app.logger.error(f"Error sending GET request to {url}: {e}")
    return None

def send_post_request(url, data=None, json=None):
  """
  Sends a POST request to the specified URL with optional data or JSON payload.

  Args:
    url (str): The URL to send the request to.
    data (dict, optional): A dictionary of form data. Defaults to None.
    json (dict, optional): A dictionary to be serialized as JSON data. Defaults to None.

  Returns:
    requests.Response: The response object from the server.
  """
  try:
    response = request_tearing_down.post(url, data=data, json=json)
    response.raise_for_status()  # Raise an exception for non-2xx status codes
    return response
  except request_finished.exceptions.RequestException as e:
    current_app.logger.error(f"Error sending POST request to {url}: {e}")
    return None

# Add more functions for PUT, DELETE, etc. as needed
def get_employee_by_id(employee_id):
  """
  Gets information about a specific employee from the server.

  Args:
    employee_id (int): The ID of the employee to retrieve.

  Returns:
    dict: A dictionary containing the employee information, or None on error.
  """
  url = f"{current_app.config['API_URL']}/employees/{employee_id}"
  response = send_get_request(url)
  if response is not None:
    return response.json()
  return None

def update_employee_profile(employee_data):
  """
  Updates an employee's profile information on the server.

  Args:
    employee_data (dict): A dictionary containing the updated employee information.

  Returns:
    bool: True if successful, False otherwise.
  """
  # Add authentication headers using current_user if using Flask-Login
  headers = {'Authorization': f"Bearer {current_user.get_token()}"}
  url = f"{current_app.config['API_URL']}/employees/{employee_data['id']}"
  response = send_post_request(url, json=employee_data, headers=headers)
  return response.status_code == 200

# Add more functions for specific API endpoints and functionalities
