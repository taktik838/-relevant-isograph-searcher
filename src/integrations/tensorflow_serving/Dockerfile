FROM ubuntu:18.04 as ubuntu
RUN apt update && apt install wget -y \
    && wget https://tfhub.dev/google/universal-sentence-encoder-multilingual/3?tf-hub-format=compressed \
        -O /embed_text_model.tar.gz

FROM tensorflow/serving

COPY --from=ubuntu /embed_text_model.tar.gz embed_text_model.tar.gz
RUN mkdir -p /models/embed_text/1 \
    && tar -xf embed_text_model.tar.gz -C /models/embed_text/1 \
    && rm embed_text_model.tar.gz

COPY models.config /models/models.config

# gRPC
EXPOSE 8500

# REST
EXPOSE 8501

ENV MODEL_CONFIG_FILE=/models/models.config
# ENV MODEL_BASE_PATH=/models
# ENV MODEL_NAME=embed_text

RUN echo '#!/bin/bash \n\n\
        tensorflow_model_server --port=8500 --rest_api_port=8501 \
        # --model_name=${MODEL_NAME} --model_base_path=${MODEL_BASE_PATH}/${MODEL_NAME}' \
        --model_config_file=${MODEL_CONFIG_FILE}' \
        > /usr/bin/tf_serving_entrypoint.sh \
    && chmod +x /usr/bin/tf_serving_entrypoint.sh

ENTRYPOINT ["/usr/bin/tf_serving_entrypoint.sh"]
