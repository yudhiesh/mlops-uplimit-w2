cd project
ray start --head
ray stop

ray metrics launch-prometheus

wget https://dl.grafana.com/enterprise/release/grafana-enterprise-11.1.4.linux-amd64.tar.gz
tar -zxvf grafana-*.tar.gz
./grafana-v11.1.4/bin/grafana-server --homepath grafana-v11.1.4 --config /tmp/ray/session_latest/metrics/grafana/grafana.ini

RAY_GRAFANA_HOST=https://redesigned-chainsaw-q655pxwjqq3r7v-3000.app.github.dev RAY_PROMETHEUS_HOST=https://redesigned-chainsaw-q655pxwjqq3r7v-9090.app.github.dev/ ray start --head

serve run src.server:entrypoint

locust -f load_test/average_test.py --host=http://127.0.0.1:8000
