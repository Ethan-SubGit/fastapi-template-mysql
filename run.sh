#!/bin/bash

# 환경 변수 설정
export ENV=${1:-production}

# Docker 컨테이너 내에서는 0.0.0.0에 바인딩해야 외부에서 접근 가능
uvicorn app.main:app --host 0.0.0.0 --port 8000 