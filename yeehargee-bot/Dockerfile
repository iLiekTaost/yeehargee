FROM registry.access.redhat.com/ubi9/ubi AS builder
# RUN curl -Lo hatch-universal.pkg \
#     https://github.com/pypa/hatch/releases/latest/download/hatch-universal.pkg

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app
COPY src/ /app/src
COPY ./pyproject.toml LICENSE.txt README.md requirements.txt /app
# ENV PROCM_IGNORE=1
# RUN apk add --no-cache python3 py3-pip && pip install --break-system-packages hatch
# RUN hatch build
# RUN apk add --no-cache python3 py3-pip && python -m venvpip install --break-system-packages --upgrade setuptools[core] build
# RUN python -m build && python 
RUN dnf install -y python3-devel
RUN python3 -m venv /app/venv
RUN source /app/venv/bin/activate
RUN pip install -r /app/requirements.txt
RUN python3 -m build
RUN pip install /app/dist/yeehargee_bot-2026.8.26-py3-none-any.whl

# # RUN python -m venv venv && \
# #     pip install -r requirements.txt && \
# #     source venv/bin/activate && \
# #     python -m build && \
# #     pip install dist/yeehargee-bot-0.0.1-py3-none-any.whl

FROM registry.access.redhat.com/ubi9/ubi
# apparently, "Each RUN instruction in a Dockerfile executes in a completely new
# shell layer. Environment changes like source or activate do not persist into
# subsequent layers or into the final ENTRYPOINT."

# this --build-arg env=env functionality doesn't seem to be working
# check `echo $VERSION`
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PATH="/app/venv/bin:$PATH"
ARG VERSION
WORKDIR /app
COPY --from=builder /app/venv /app/venv
ENV VERSION=${VERSION}
ENTRYPOINT ["/app/venv/bin/python", "-m", "yeehargee-bot"]

# ENTRYPOINT ["source /app/venv/bin/activate"]
CMD ["-h"]
