#Python base image
FROM public.ecr.aws/lambda/python:3.12

#For all the dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}

#Install libraries
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copying our source code
COPY agent.py ${LAMBDA_TASK_ROOT}
COPY lambda_function.py ${LAMBDA_TASK_ROOT}
COPY ingest.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler
CMD [ "lambda_function.lambda_handler" ]