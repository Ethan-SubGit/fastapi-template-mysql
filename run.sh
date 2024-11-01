#!/bin/bash

# 환경 변수 설정
export ENV=${1:-development}

# 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 