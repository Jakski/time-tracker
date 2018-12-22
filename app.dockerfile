FROM python:3.5

ARG HOME_DIR=/home/developer
ARG USER_ID=1000
ARG GROUP_ID=1000

ENV PATH "${HOME_DIR}/.local/bin:$PATH"

RUN groupadd --gid $GROUP_ID developer \
	&& useradd \
		--shell /bin/bash \
		--gid $USER_ID \
		--uid $GROUP_ID \
		--create-home \
		--home-dir "${HOME_DIR}" \
		developer

COPY requirements.txt "/tmp/requirements.txt"

USER $USER_ID:$GROUP_ID

RUN pip install --user tox \
	&& pip install --user -r "/tmp/requirements.txt"

VOLUME "${HOME_DIR}/time-tracker"
