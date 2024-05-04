import io
import json
import os
import requests

from time import sleep
from typing import List, Optional, Union, Dict
from urllib.parse import urlencode

from tonic_textual.classes.api_responses.single_detection_result import SingleDetectionResult
from tonic_textual.classes.custom_model import CustomModel
from tonic_textual.classes.httpclient import HttpClient
from tonic_textual.classes.api_responses.redaction_response import RedactionResponse
from tonic_textual.enums.pii_state import PiiState
from tonic_textual.services.dataset import DatasetService
from tonic_textual.services.datasetfile import DatasetFileService
from tonic_textual.classes.dataset import Dataset
from tonic_textual.classes.datasetfile import DatasetFile
from tonic_textual.classes.tonic_exception import DatasetNameAlreadyExists, InvalidJsonForRedactionRequest, FileNotReadyForDownload

class TonicTextual:
    '''Wrapper class for invoking Tonic Textual API

    Parameters
    ----------
    base_url : str
        The URL to your Tonic Textual instance. Do not include trailing backslashes.
    api_key : str
        Your API token. This argument is optional. Instead of providing the API token here, it is recommended that you set the API key in your environment as the value of TONIC_TEXTUAL_API_KEY.
    verify: bool
        Whether SSL Certification verification is performed.  This is enabled by default.
    Examples
    --------
    >>> TonicTextual("http://localhost:3000")
    '''
    def __init__(self, base_url : str, api_key: Optional[str] = None, verify: bool = True):
        if api_key is None:
            api_key = os.environ.get("TONIC_TEXTUAL_API_KEY")
            if api_key is None:
                raise Exception("No API key provided. Either provide an API key, or set the API key as the value of the TONIC_TEXTUAL_API_KEY environment variable.")
        self.api_key = api_key
        self.client = HttpClient(base_url, self.api_key, verify)
        self.dataset_service = DatasetService(self.client)
        self.datasetfile_service = DatasetFileService(self.client)
        self.verify = verify

    @staticmethod
    def _validate_generator_options(generator_default: PiiState, generator_config: Dict[str, PiiState]) -> None:
        invalid_pii_states = [v for v in list(generator_config.values()) if v not in PiiState._member_names_]
        if(len(invalid_pii_states)>0):
            raise Exception("Invalid configuration for generator_config. The allowed values are Off, Synthesis, and Redaction.")
        if generator_default not in PiiState._member_names_:
            raise Exception("Invalid option for generator_default. The allowed values are Off, Synthesis, and Redaction.")

    def create_dataset(self, dataset_name:str):
        """Creates a dataset. A dataset is a collection of 1 or more files for Tonic Textual to scan and redact.

        Parameters
        -----
        dataset_name : str
            The name of the dataset. Dataset names must be unique.


        Returns
        -------
        Dataset
            The newly created dataset.


        Raises
        ------

        DatasetNameAlreadyExists
            Raised if a dataset with the same name already exists.

        """
        try:
            self.client.http_post("/api/dataset", data={"name": dataset_name})
        except requests.exceptions.HTTPError as e:
            if e.response.status_code==409:
                raise DatasetNameAlreadyExists(e)

        return self.get_dataset(dataset_name)

    def delete_dataset(self, dataset_name: str):
        params = { "datasetName": dataset_name}
        self.client.http_delete("/api/dataset/delete_dataset_by_name?" + urlencode(params))




    def get_dataset(self, dataset_name : str) -> Dataset:
        '''Gets the dataset for the specified dataset name.

        Parameters
        ----------
        dataset_name : str
            The name of the dataset.

        Returns
        -------
        Dataset

        Examples
        --------
        >>> dataset = tonic.get_dataset("llama_2_chatbot_finetune_v5")
        '''
        return self.dataset_service.get_dataset(dataset_name)

    def get_files(self, dataset_id: str) -> List[DatasetFile]:
        """
        Gets all of the files in the dataset.

        Returns
        ------
        List[DatasetFile]
        A list of all of the files in the dataset.
        """
        return self.datasetfile_service.get_files(dataset_id)

    def unredact_bulk(self, redacted_strings: List[str], random_seed: Optional[int] = None) -> List[str]:
            """Removes redaction from a list of strings. Returns the strings with the original values.

            Parameters
            ----------
            redacted_strings : List[str]
                The list of redacted strings from which to remove the redaction.

            random_seed: Optional[int] = None
                An optional value to use to override Textual's default random number seeding.  Can be used to ensure that different API calls use the same or different random seeds.

            Returns
            -------
            List[str]
                The list of strings with the redaction removed.
            """

            if random_seed is not None:
                additional_headers = {'textual-random-seed':str(random_seed)}
            else:
                additional_headers = {}
                
            response = self.client.http_post("/api/unredact", data=redacted_strings, additional_headers=additional_headers)
            return response

    def unredact(self, redacted_string: str, random_seed: Optional[int] = None) -> str:
            """Removes the redaction from a provided string. Returns the string with the original values.

            Parameters
            ----------
            redacted_string : str
                The redacted string from which to remove the redaction.

            random_seed: Optional[int] = None
                An optional value to use to override Textual's default random number seeding.  Can be used to ensure that different API calls use the same or different random seeds.
            
            Returns
            -------
            str
                The string with the redaction removed.
            """


            if random_seed is not None:
                additional_headers = {'textual-random-seed':str(random_seed)}
            else:
                additional_headers = {}
                
            response = self.client.http_post("/api/unredact", data=[redacted_string], additional_headers=additional_headers)

            
            return response

    def redact(self, string: str, generator_config: Dict[str, PiiState] = dict(), generator_default: PiiState = PiiState.Redaction, custom_models: List[str] = [], random_seed: Optional[int] = None) -> RedactionResponse:
            """Redacts a string. Depending on the configured handling for each sensitive data type, values can be either redacted, synthesized, or ignored.

            Parameters
            ----------
            string : str
                The string to redact.

            generator_config: Dict[str, PiiState]
                A dictionary of sensitive data entities. For each entity, indicates whether to redact, synthesize, or ignore it.
                Values must be one of "Redaction", "Synthesis", or "Off".

            generator_default: PiiState = PiiState.Redaction
                The default redaction used for all types not specified in generator_config.
                Values must be one of "Redaction", "Synthesis", or "Off".

            custom_models: List[str] = []
                A list of custom model names to use to identify values to redact. To see the list of custom models that you have access to, use the get_custom_models function.

            random_seed: Optional[int] = None
                An optional value to use to override Textual's default random number seeding.  Can be used to ensure that different API calls use the same or different random seeds.

            Returns
            -------
            RedactionResponse
                The redacted string along with ancillary information.

            Examples
            --------
                >>> textual.redact("John Smith is a person", generator_config= {"NAME_GIVEN": "Redaction"}, generator_default="Off") # only redacts NAME_GIVEN

            """

            self._validate_generator_options(generator_default, generator_config)
            endpoint = "/api/redact"

            if random_seed is not None:
                additional_headers = {'textual-random-seed':str(random_seed)}
            else:
                additional_headers = {}
                
            response = self.client.http_post(endpoint, data={"text": string, "generatorDefault": generator_default, "generatorConfig": generator_config, "customModels": custom_models}, additional_headers=additional_headers)
            de_id_results = [SingleDetectionResult(x["start"], x["end"], x["label"], x["text"], x["score"]) for x in list(response["deIdentifyResults"])]

            return RedactionResponse(response["originalText"], response["redactedText"], response["usage"], de_id_results)

    def llm_synthesis(self, string: str, generator_config: Dict[str, PiiState] = dict(), generator_default: PiiState = PiiState.Redaction) -> RedactionResponse:
        """Deidentifies a string by redacting sensitive data and replacing these values with values generated by an LLM.

        Parameters
        ----------
        string : str
                The string to redact.

        generator_config: Dict[str, PiiState]
                A dictionary of sensitive data entities. For each entity, indicates whether to redact, synthesize, or ignore it.

        generator_default: PiiState = PiiState.Redaction
            The default redaction used for all types not specified in generator_config.

       Returns
        -------
                The de-identified string
        """
        self._validate_generator_options(generator_default, generator_config)
        endpoint = "/api/synthesis"
        response = self.client.http_post(endpoint, data={"text": string, "generatorDefault": generator_default, "generatorConfig": generator_config})

        de_id_results = [SingleDetectionResult(x["start"], x["end"], x["label"], x["text"], x["score"]) for x in
                         list(response["deIdentifyResults"])]

        return RedactionResponse(response["originalText"], response["redactedText"], response["usage"], de_id_results)

    def redact_json(self, json_data: Union[str, dict], generator_config:Dict[str, PiiState] = dict(), generator_default: PiiState = PiiState.Redaction, custom_models: List[str] = [], random_seed: Optional[int] = None) -> RedactionResponse:
        """Redacts the values in a JSON blob. Depending on the configured handling for each sensitive data type, values can be either redacted, synthesized, or ignored.

        Parameters
        ----------
        json_string : Union[str, dict]
            The JSON whose values will be redacted.  This can be either a JSON string or a Python dictionary

        generator_config: Dict[str, PiiState]
                A dictionary of sensitive data entities. For each entity, indicates whether to redact, synthesize, or ignore it.

        generator_default: PiiState = PiiState.Redaction
                The default redaction used for all types not specified in generator_config.

        custom_models: List[str] = []
            A list of custom model names to use to identify values to redact. To see the list of custom models that you have access to, use the get_custom_models function.

        random_seed: Optional[int] = None
            An optional value to use to override Textual's default random number seeding.  Can be used to ensure that different API calls use the same or different random seeds.

        Returns
        -------
        RedactionResponse
            The redacted string along with ancillary information.
        """
        self._validate_generator_options(generator_default, generator_config)
        endpoint = "/api/redact/json"

        if isinstance(json_data, str):
            json_text = json_data
        elif isinstance(json_data, dict):
            json_text = json.dumps(json_data)
        else:
            raise Exception(f'redact_json must receive either a JSON blob as a string or dict().  You passed in type {type(json_data)} which is not supported')
        payload = {"jsonText": json_text, "generatorDefault":generator_default, "generatorConfig": generator_config, "customModels": custom_models}

        try:
            if random_seed is not None:
                additional_headers = {'textual-random-seed':str(random_seed)}
            else:
                additional_headers = {}
            response = self.client.http_post(endpoint, data=payload, additional_headers=additional_headers)
        except requests.exceptions.HTTPError as e:
             if e.response.status_code==400:
                  raise InvalidJsonForRedactionRequest(e.response.text)
             raise e

        de_id_results = [SingleDetectionResult(x["start"], x["end"], x["label"], x["text"], x["score"], x["jsonPath"]) for x in list(response["deIdentifyResults"])]

        return RedactionResponse(response["originalText"], response["redactedText"], response["usage"], de_id_results)

    def get_custom_models(self) -> List[CustomModel]:
        """Returns all of the custom models that the user owns.

        Returns
        -------
        List[CustomModel]
            A list of all of the custom models that the user owns.
        """

        with requests.Session() as session:
            response = self.client.http_get("/api/models", session=session)
            models: List[CustomModel] = []
            for model in response:
                id = model['id']
                name = model['name']
                entities = model['entities']
                entityNames = [entity['label'] for entity in entities]
                models.append(CustomModel(id, name, entityNames))

            return models

    def start_file_redaction(self, file: io.IOBase, file_name: str) -> str:
        """
        Redact a provided file

        Parameters
        --------
        file: io.IOBase
            The opened file, available for reading, which will be uploaded and redacted
        file_name: str
            The name of the file

        Returns
        -------
        str
        The job id which can be used to download the redacted file once it is ready

        """

        files = {
            'document': (None, json.dumps({"fileName": file_name, "csvConfig":{}, "datasetId":""}), 'application/json'),
            'file': file
        }

        response = self.client.http_post("/api/unattachedfile/upload", files=files)

        return response['jobId']

    def download_redacted_file(self, job_id: str, generator_config: Dict[str, PiiState] = dict(), generator_default: PiiState = PiiState.Redaction, custom_models: List[str] = [], random_seed: Optional[int] = None, num_retries: int = 6) -> bytes:
        """
        Download a redacted file

        Parameters
        --------
        job_id: str
            The ID of the redaction job

        generator_config: Dict[str, PiiState]
                A dictionary of sensitive data entities. For each entity, indicates whether to redact, synthesize, or ignore it.

        generator_default: PiiState = PiiState.Redaction
                The default redaction used for all types not specified in generator_config.

        custom_models: List[str] = []
            A list of custom model names to use to identify values to redact. To see the list of custom models that you have access to, use the get_custom_models function.

        random_seed: Optional[int] = None
            An optional value to use to override Textual's default random number seeding.  Can be used to ensure that different API calls use the same or different random seeds.

        num_retries: int = 6
            An optional value to specify how many times to attempt to download the file.  If a file is not yet ready for download, there will be a 10 second pause before retrying.  (The default value is 6)

        Returns
        -------
        bytes
            The redacted file as byte array
        """
        self._validate_generator_options(generator_default, generator_config)
        retries = 1
        while(retries <= num_retries):
            try:
                if random_seed is not None:
                    additional_headers = {'textual-random-seed':str(random_seed)}
                else:
                    additional_headers = {}
                return self.client.http_post_download_file(f"/api/unattachedfile/{job_id}/download", data={"generatorDefault": generator_default, "generatorConfig": generator_config, "customModels": custom_models}, additional_headers=additional_headers )
                
            
            except FileNotReadyForDownload:
                 retries = retries + 1
                 if retries <= num_retries:
                    sleep(10)

        retryWord = "retry" if num_retries==1 else "retries"
        raise FileNotReadyForDownload(f"After {num_retries} {retryWord} the file is not yet ready for download.  This is likely due to a high service load.  Please try again later.")
