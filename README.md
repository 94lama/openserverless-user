# Setup

Assumo hai installato miniops.me

Esporta il kubeconfig con `ops util kubeconfig`

Convertilo ed encodalo in base64 e mettilo nel .env con

echo KUBECONFIG=$(sed -e 's!server: .*!server: https://kubernetes.default.svc.cluster.local!' ~/.kube/config | base64 -b 0) >>.env

Fai il deploy:

ops ide deploy


La function hello ora riesce ad accedere al kube (esempio che lista i namespace)
