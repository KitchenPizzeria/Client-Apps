FROM python:3

RUN pip install --upgrade pip && \
    pip install ttkthemes && \
    pip install numpy

WORKDIR /user/joseph/Desktop/DIY-DIGITISED
COPY . .
CMD ["Main.py"]
ENTRYPOINT ["python3"]