from typing import Dict, List, Union

from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

def predict_custom_trained_model_sample(
    project: str,
    endpoint_id: str,
    instances: Union[Dict, List[Dict]],
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    """
    `instances` can be either single instance of type dict or a list
    of instances.
    """
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    # The format of each instance should conform to the deployed model's prediction input schema.
    instances = instances if isinstance(instances, list) else [instances]
    instances = [
        json_format.ParseDict(instance_dict, Value()) for instance_dict in instances
    ]
    parameters_dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    # The predictions are a google.protobuf.Value representation of the model's predictions.
    return response.predictions[0]


class GemmaBot():
  __START_TURN_USER__ = "<start_of_turn>user\n"
  __START_TURN_MODEL__ = "<start_of_turn>model\n"
  __END_TURN__ = "<end_of_turn>\n"

  def __init__(self, system=""):
    self.system = system
    self.history = []

  def add_to_history_as_user(self, message):
      self.history.append(self.__START_TURN_USER__ + message + self.__END_TURN__)

  def add_to_history_as_model(self, message):
      self.history.append(self.__START_TURN_MODEL__ + message + self.__END_TURN__)

  def get_history(self):
      return "".join([*self.history])

  def get_full_prompt(self):
    prompt = self.get_history() + self.__START_TURN_MODEL__
    if len(self.system)>0:
      prompt = self.system + "\n" + prompt
    return prompt

  def ask(self, message):
    self.add_to_history_as_user(message)
    prompt = self.get_full_prompt()
    response = predict_custom_trained_model_sample(
      project="<YOUR_PROJECT_ID>",
      endpoint_id="<YOUR_ENDPONT_ID>",
      location="<YOUR_LOCATION>",
      api_endpoint="<YOUR_LOCATION>-aiplatform.googleapis.com",
      instances={ "prompt": prompt, "max_tokens": 2048 }
      )[8:]
    result = response.replace(prompt, "")[8:]  # Extract only the new response
    self.add_to_history_as_model(result)
    return result

