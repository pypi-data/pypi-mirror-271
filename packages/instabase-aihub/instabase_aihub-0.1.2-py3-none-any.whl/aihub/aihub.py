from aihub.api.batch_api import BatchApi
from aihub.api.conversation_api import ConversationApi
from aihub.api.run_api import RunApi
from aihub.api_client import ApiClient
import os


class AIHub:

  def __init__(self,
               api_key,
               ib_context=None,
               api_root='https://aihub.instabase.com/api',
               debug=False):
    self.client = ApiClient()
    self.client.configuration.host = api_root
    self.client.configuration.access_token = api_key
    self.client.configuration.debug = debug
    self.batches = self.Batches(BatchApi(self.client), ib_context)
    self.conversations = self.Conversations(
        ConversationApi(self.client), ib_context)
    self.apps = self.Apps(RunApi(self.client), ib_context)

  class Batches:

    def __init__(self, api_instance, ib_context):
      self.api_instance = api_instance
      self.ib_context = ib_context

    def create(self, name, workspace_name=None):
      batch = self.api_instance.create_batch(
          {
              'name': name,
              'workspace_name': workspace_name
          },
          ib_context=self.ib_context)
      return batch

    def list(self, workspace=None, username=None, limit=None, offset=None):
      response = self.api_instance.list_batches(
          workspace=workspace,
          username=username,
          limit=limit,
          offset=offset,
          ib_context=self.ib_context)
      return response

    def get(self, id):
      response = self.api_instance.get_batch(id, ib_context=self.ib_context)
      return response

    def delete(self, id):
      response = self.api_instance.delete_batch(id, ib_context=self.ib_context)
      return response

    def add_file(self, id, file_name, file):
      self.api_instance.add_file_to_batch(
          id, file_name, file.read(), ib_context=self.ib_context)

    def delete_file(self, id, file_name):
      response = self.api_instance.delete_file_from_batch(
          id, file_name, ib_context=self.ib_context)
      return response

    def poll_job(self, id):
      response = self.api_instance.poll_batches_job(
          id, ib_context=self.ib_context)
      return response

  class Conversations:

    def __init__(self, api_instance, ib_context):
      self.api_instance = api_instance
      self.ib_context = ib_context

    def create(self,
               name,
               description=None,
               files=[],
               org=None,
               workspace=None,
               enable_object_detection=None):
      response = self.api_instance.create_conversation(
          name=name,
          description=description,
          files=files,
          org=org,
          workspace=workspace,
          enable_object_detection=enable_object_detection,
          ib_context=self.ib_context)
      return response

    def status(self, conversation_id):
      status = self.api_instance.get_conversation(
          conversation_id, ib_context=self.ib_context)
      return status

    def update(self, conversation_id, name=None, description=None):
      response = self.api_instance.update_conversation(
          conversation_id,
          name=name,
          description=description,
          ib_context=self.ib_context)
      return response

    def list(self):
      conversations = self.api_instance.list_conversations(
          ib_context=self.ib_context)
      return conversations

    def converse(self, conversation_id, question, document_ids):
      answer = self.api_instance.converse(
          conversation_id, {
              'question': question,
              'document_ids': document_ids,
              'mode': 'default'
          },
          ib_context=self.ib_context)
      return answer

    def add_documents(self, conversation_id, files, process_files=True):
      response = self.api_instance.add_documents_to_conversation(
          conversation_id, files, process_files, ib_context=self.ib_context)
      return response

    def delete_documents(self, conversation_id, ids):
      response = self.api_instance.delete_documents_from_conversation(
          conversation_id, {'ids': ids}, ib_context=self.ib_context)
      return response

    def get_document_metadata(self, conversation_id, document_id):
      response = self.api_instance.get_conversation_document_metadata(
          conversation_id, document_id, ib_context=self.ib_context)
      return response

  class Runs:

    def __init__(self, api_instance, ib_context):
      self.api_instance = api_instance
      self.ib_context = ib_context

    def run(self, app_name=None, files=[], app_id=None, settings=None):
      results = self.api_instance.run_app_sync(
          app_name=app_name,
          files=files,
          app_id=app_id,
          settings=settings,
          ib_context=self.ib_context)
      return results

    def create(self,
               app_name=None,
               batch_id=None,
               app_id=None,
               input_dir=None,
               output_dir=None,
               settings=None):
      # Validate that one of batch_id or input_dir is provided
      if not batch_id and not input_dir:
        raise ValueError("Either batch_id or input_dir is required.")

      # Construct the dictionary with only the set values
      run_details = {}
      if app_name:
        run_details['app_name'] = app_name
      elif app_id:  # Use elif because only one of them needs to be set
        run_details['app_id'] = app_id

      if batch_id:
        run_details['batch_id'] = batch_id
      elif input_dir:  # Use elif for the same reason
        run_details['input_dir'] = input_dir
      run_details['output_dir'] = output_dir
      run_details['settings'] = settings
      # Call run_app with the constructed dictionary
      run = self.api_instance.run_app(run_details, ib_context=self.ib_context)
      return run

    def status(self, id):
      status = self.api_instance.get_run_status(id, ib_context=self.ib_context)
      return status

    def results(self,
                id,
                file_offset=None,
                include_confidence_scores=False,
                include_source_info=False):
      results = self.api_instance.get_run_results(
          id=id,
          file_offset=file_offset,
          include_confidence_scores=include_confidence_scores,
          include_source_info=include_source_info,
          ib_context=self.ib_context)
      return results

  class Apps:

    def __init__(self, api_instance, ib_context):
      self.api_instance = api_instance
      self.ib_context = ib_context
      self.runs = AIHub.Runs(api_instance, ib_context)
