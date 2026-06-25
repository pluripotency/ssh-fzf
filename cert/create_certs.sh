#!/bin/bash
CURRENT=$(cd $(dirname $0);pwd)

# certディレクトリのパス
CERT_DIR=$CURRENT
KEY_FILE="${CERT_DIR}/key.pem"
CERT_FILE="${CERT_DIR}/cert.pem"

# certディレクトリが存在しない場合は作成
if [ ! -d "${CERT_DIR}" ]; then
  mkdir -p "${CERT_DIR}"
  echo "Created directory: ${CERT_DIR}"
fi

# key.pemまたはcert.pemのどちらか一方でも存在する場合は作成しない
if [ -f "${KEY_FILE}" ] || [ -f "${CERT_FILE}" ]; then
  echo "Certificate generation skipped: '${KEY_FILE}' or '${CERT_FILE}' already exists."
  exit 0
fi

# 自己署名証明書の生成
echo "Generating self-signed certificate (key.pem and cert.pem)..."
openssl req -x509 -newkey rsa:4096 -keyout "${KEY_FILE}" -out "${CERT_FILE}" -sha256 -days 365 -nodes -subj "/CN=localhost" -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

if [ $? -eq 0 ]; then
  echo "Successfully generated certificate and key in ${CERT_DIR}/"
else
  echo "Error: Failed to generate certificate and key."
  exit 1
fi
