from uuid import uuid4
from therix.core.pipeline_component import PipelineComponent
from .constants import DataSourceMaster, EmbeddingModelMaster, PipelineTypeMaster  # Import your constants
from ..services.pipeline_service import PipelineService  # Import your service
from ..entities.models import ConfigType  # Import your ConfigType enum
from ..services.pipeline_service import PipelineService  # Import your service
from langchain.globals import set_llm_cache
from therix.core.response import ModelResponse
from sqlalchemy import  create_engine
from therix.core.cache import TherixCache
from therix.db.session import SQLALCHEMY_DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

class Pipeline:

    def __init__(self, name, status="IN_DRAFT"):
        self.pipeline_data = {"name": name, "status": status}
        self.components = []
        self.type = None
        self.pipeline_service = PipelineService()

    @classmethod
    def from_id(cls, pipeline_id):
        pipeline = cls.__new__(cls)
        pipeline.__init__(None)
        pipeline.load(pipeline_id)
        return pipeline

    def add(self, component):
        if not isinstance(component, PipelineComponent):
            raise ValueError("component must be an instance of PipelineComponent")
        
        component_type_to_pipeline_type = {
            ConfigType.EMBEDDING_MODEL.value: PipelineTypeMaster.RAG.value,
            ConfigType.SUMMARIZER.value: PipelineTypeMaster.SUMMARIZER.value,
            # Add future component types here
        }

        # Check if the component type is in the dictionary and if the pipeline type is not set
        if component.type.value in component_type_to_pipeline_type and self.type is None:
            self.type = component_type_to_pipeline_type[component.type.value]
        elif component.type.value not in component_type_to_pipeline_type:
            pass
        else:
            raise Exception(f'Cannot add {component.type.value}.')
        
        self.components.append(component)
        return self  # Enable method chaining

    def add_data_source(self, name, config):
        data_source = PipelineComponent(ConfigType.INPUT_SOURCE, name, config)
        return self.add(data_source)

    def add_embedding_model(self, name, config):
        embedding_model = PipelineComponent(ConfigType.EMBEDDING_MODEL, name, config)
        return self.add(embedding_model)

    def add_inference_model(self, name, config):
        inference_model = PipelineComponent(ConfigType.INFERENCE_MODEL, name, config)
        return self.add(inference_model)

    def add_output_source(self, name, config):
        output_source = PipelineComponent(ConfigType.OUTPUT_SOURCE, name, config)
        return self.add(output_source)

    def save(self):
        configurations_data = [
            {
                "config_type": component.type.value,
                "name": component.name,
                "config": component.config,
            }
            for component in self.components
        ]
        self.pipeline_data['type'] = self.type
        # Save the pipeline and its components to the database
        self.pipeline_data = self.pipeline_service.create_pipeline_with_configurations(
            self.pipeline_data, configurations_data
        )
        self.id = self.pipeline_data.id
        self.name = self.pipeline_data.name
        return self.pipeline_data

    def publish(self):
        return self.pipeline_service.publish_pipeline(self.pipeline_data)

    def load(self, pipeline_id):
        self.pipeline_data = self.pipeline_service.get_pipeline(pipeline_id)
        self.id = self.pipeline_data.id
        self.name = self.pipeline_data.name
        return self.pipeline_data

    def preprocess_data(self):
        self.pipeline_service.preprocess_data(self.pipeline_data.id)

    def invoke(self, question, session_id=None):
            cached_response = None
            therix_cache = TherixCache(engine)
            inference_model = self.pipeline_service.get_pipeline_configuraitons_by_type(self.pipeline_data.id, ConfigType.INFERENCE_MODEL)

            if session_id is None:
                session_id = uuid4()
            add_cache = self.pipeline_service.get_pipeline_configuraitons_by_type(self.pipeline_data.id, ConfigType.CACHE_CONFIG)
            

            pipeline_trace_config = self.pipeline_service.get_pipeline_configuraitons_by_type(
                self.pipeline_data.id, ConfigType.TRACE_DETAILS
            )
            trace_details = pipeline_trace_config[0].config if pipeline_trace_config else None

            pipeline_type = self.pipeline_service.get_pipeline(self.pipeline_data.id).type.value
            model_response = ModelResponse()

            if pipeline_type == PipelineTypeMaster.RAG.value:
                if add_cache:
                    cached_response = therix_cache.lookup(question, inference_model[0].name, self.pipeline_data.id)
                if cached_response:
                    print("from cache", cached_response)
                    return ModelResponse(cached_response.response, session_id).create_response
                answer = self.pipeline_service.invoke_pipeline(
                    self.pipeline_data.id, question, session_id, trace_details
                )
                if add_cache:
                    therix_cache.update(question, inference_model[0].name, answer, self.pipeline_data.id)
            elif pipeline_type == PipelineTypeMaster.SUMMARIZER.value:
                answer = self.pipeline_service.invoke_summarizer_pipeline(self.pipeline_data.id, text=question)
            
            return ModelResponse(answer, session_id).create_response()
            
